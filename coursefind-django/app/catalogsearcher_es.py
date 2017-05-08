import datetime
import re
import copy
import random
import json
from functools import wraps

try:
    from . import cmu_info, cmu_prof
    from .utilities import *
    from .coursescotty import *
except:
    import cmu_info, cmu_prof
    from utilities import *
    from coursescotty import *

from elasticsearch import Elasticsearch
import elasticsearch


ALL_COURSES_INDEX = "all_courses"


class LecsecFilter():
    def filterPittsburgh(func):
        def f(*args, **kwargs):
            def filterFunc(event):
                return event.times[0].get("location") == "Pittsburgh, Pennsylvania"
            d = func(*args, **kwargs)
            newDict = dict()
            for key, L in d.items():
                newDict[key] = list(filter(filterFunc, L))
            return newDict
        return f

    def filterMini(mini=0):
        assert(isinstance(mini, int))
        if mini == 0:
            mini = getMini()

        def filterMini_decorator(func):
            @wraps(func)
            def f(*args, **kwargs):
                d = func(*args, **kwargs)
                newDict = dict()
                for key, L in d.items():
                    newL = []
                    for event in L:
                        _sem = 0
                        match = re.search("(\d|[a-zA-Z])(\d)", event.lecsec)
                        if match:
                            # mini lecture or section
                            _sem = int(match.group(2))
                        if _sem == 0 or _sem == mini:
                            newL.append(event)
                    newDict[key] = newL
                return newDict
            return f
        return filterMini_decorator


##
## @brief      The Searcher object that parses input and generates queries.
##
class Searcher(object):

    ##
    ## @brief      init
    ##
    ## @param      self
    ## @param      s           The query text
    ##
    def __init__(self, s=""):
        s = s.strip()
        if len(s) > 140:
            self.text = s[:140]
        else:
            self.text = s

        self.rawQuery = dict()
        parser = Parser(s)
        self.searchable = parser.searchable
        self.length = parser.length
        self.rawQuery = parser.rawQuery

    def __repr__(self):
        return "<Searcher Object: text={}, rawQuery={}>".format(repr(self.text), repr(self.rawQuery))

    ##
    ## @brief      Generate the query for the database.
    ##
    ## @return     (dict) The query for querying the database.
    ##
    def generateQuery(self):
        return self.constructESQueryFromRaw(self.rawQuery)

    @staticmethod
    def constructESQueryFromRaw(raw_query):

        def cleanUp(query):
            if (query["query"]["bool"]["filter"]["or"][0]
                    ["nested"]["query"]["bool"]["must"]
                    ["nested"]["query"]["bool"]["must"] == []):
                for i in range(0, 2):
                    del query["query"]["bool"]["filter"]["or"][i]\
                             ["nested"]["query"]["bool"]["must"]
                if "should" not in query["query"]["bool"]["filter"]["or"][i]\
                                        ["nested"]["query"]["bool"]:
                    del query["query"]["bool"]["filter"]
            return query

# DEBUG
        print(raw_query)

        QUERY_BASE = '''
        {
           "query": {
              "bool": {
                 "filter": {
                    "or": [
                       {
                          "nested": {
                             "inner_hits": {},
                             "path": "lectures",
                             "score_mode": "avg",
                             "query": {
                                "bool": {
                                   "must":
                                      {
                                         "nested": {
                                            "path": "lectures.times",
                                            "score_mode": "avg",
                                            "query": {
                                               "bool": {
                                                  "must": []
                                               }
                                            }
                                         }
                                      }

                                }
                             }
                          }
                       },
                       {
                          "nested": {
                             "inner_hits": {},
                             "path": "sections",
                             "score_mode": "avg",
                             "query": {
                                "bool": {
                                   "must":
                                      {
                                         "nested": {
                                            "path": "sections.times",
                                            "score_mode": "avg",
                                            "query": {
                                               "bool": {
                                                  "must": []
                                               }
                                            }
                                         }
                                      }

                                }
                             }
                          }
                       }
                    ]
                 }
              }
           }
        }
        '''

        query = json.loads(QUERY_BASE)

        if "rest" in raw_query:
            query["query"]["bool"]["must"] = {"query_string": {
                                                "query": raw_query["rest"][0]}}
            query["query"]["bool"]["should"] = [
                                                {"match": {"id": raw_query["rest"][0]}},
                                                {"match": {"name": raw_query["rest"][0]}}
                                                ]
        elif "courseid" in raw_query:
            # query["query"]["bool"]["must"] = {"term": {"id": raw_query["courseid"]}}
            query["query"]["bool"]["must"] = {"match": {"id": {
                                                "query": raw_query["courseid"][0],
                                                "operator": "and",
                                                "boost": 2}}}

        else:
            query["query"]["bool"]["must"] = {"match_all": {}}

        # fields: day, building, room, instructor
        if "day" in raw_query: # must
            query["query"]["bool"]["filter"]["or"][0]\
                 ["nested"]["query"]["bool"]["must"]\
                 ["nested"]["query"]["bool"]["must"].append(
                    {"match": {"lectures.times.days": raw_query["day"][0]}})
            query["query"]["bool"]["filter"]["or"][1]\
                 ["nested"]["query"]["bool"]["must"]\
                 ["nested"]["query"]["bool"]["must"].append(
                    {"match": {"sections.times.days": raw_query["day"][0]}})

        if "building" in raw_query: # must
            query["query"]["bool"]["filter"]["or"][0]\
                 ["nested"]["query"]["bool"]["must"]\
                 ["nested"]["query"]["bool"]["must"].append(
                    {"match": {"lectures.times.building": raw_query["building"][0]}})
            query["query"]["bool"]["filter"]["or"][1]\
                 ["nested"]["query"]["bool"]["must"]\
                 ["nested"]["query"]["bool"]["must"].append(
                    {"match": {"sections.times.building": raw_query["building"][0]}})

        if "room" in raw_query: # must
            query["query"]["bool"]["filter"]["or"][0]\
                 ["nested"]["query"]["bool"]["must"]\
                 ["nested"]["query"]["bool"]["must"].append(
                    {"match": {"lectures.times.room": raw_query["room"][0]}})
            query["query"]["bool"]["filter"]["or"][1]\
                 ["nested"]["query"]["bool"]["must"]\
                 ["nested"]["query"]["bool"]["must"].append(
                    {"match": {"sections.times.room": raw_query["room"][0]}})

        if "instructor" in raw_query: # should
            for i in range(0, 2):
                query["query"]["bool"]["filter"]["or"][i]\
                     ["nested"]["query"]["bool"]["should"] = []

            query["query"]["bool"]["filter"]["or"][0]\
                 ["nested"]["query"]["bool"]["should"].append(
                    {"match": {"lectures.instructors": raw_query["instructor"][0]}})
            query["query"]["bool"]["filter"]["or"][1]\
                 ["nested"]["query"]["bool"]["should"].append(
                    {"match": {"sections.instructors": raw_query["instructor"][0]}})

        query = cleanUp(query)

        return query


class Parser(object):
    def __init__(self, text):
        if len(text) > 140:
            self.text = text[:140]
        else:
            self.text = text
        self.rawQuery = Listdict()
        self.searchable = splitString(self.text.lower(), " ")
        self.length = len(self.searchable)
        self.parse()

    def __repr__(self):
        return "<Parser Object: text={}, rawQuery={}>".format(repr(self.text), repr(self.rawQuery))


    ##
    ## @brief      Constructs the query for a given field.
    ##
    ## @param      s      (str) Input text
    ## @param      field  (str) The specified field type
    ##
    ## @return     Returns a dictionary of results with field as the key.
    ##
    @staticmethod
    def getField(s, field):
        result = dict()
# DEBUG
        # print("##s:", s, field)
        # Match course id in forms of "36217" or "36-217"
        if field == "courseid":
            if s.isdigit():
                if len(s) == 5:
                    result[field] = [(s[:2] + "-" + s[2:])]
            else:
                match = re.search("\d\d-\d\d\d", s)
                if match:
                    result[field] = [match.group()]
                else:
                    return None

        # Match building in forms of "BH136A"
        if field == "building_room":
            match = re.search("^([a-zA-Z]{2})(\w?\d+\w?)", s)
            # "BH136A", "HHA104"
            if match:
                if match.group(1) in cmu_info.CMU_BUILDINGS_ABBR:
                    result["building"] = [match.group(1).upper()]
                    result["room"] = [match.group(2).upper()]
            # "GHC4102"
                else:
                    match = re.search("^([a-zA-Z]{3})(\w?\d+\w?)", s)
                    if match:
                        result["building"] = [match.group(1).upper()]
                        result["room"] = [match.group(2).upper()]
            if not match:
                return None

        if field == "building":
            if s in cmu_info.CMU_BUILDINGS:
                result[field] = [cmu_info.CMU_BUILDINGS[s]]
            elif s in cmu_info.CMU_BUILDINGS_ABBR:
                result[field] = [s.upper()]
            else:
                return None

        if field == "day":
            if s in cmu_info.DAYS_STRING:
                result[field] = [cmu_info.DAYS_STRING[s]]
            else:
                return None

        if field == "instructor":
            # see if the string is a part of the name of a instructor
            # could be first name or last name or both
            if s in cmu_prof.NAMES:
                result[field] = [s]
            else:
                return None

        return result if result != dict() else None

    ##
    ## @brief      Gets the query for a specified from the searchable list
    ##
    ## @param      self        The object
    ## @param      searchable  The searchable list consists of strings as
    ##                         elements
    ## @param      field       The specified field
    ## @param      multiple  Whether or not to look for multiple results
    ##
    ## @return     A list of query strings if found, None if nothing is found.
    ##
    def getFieldFromList(self, searchable, field):
# DEBUG
        # print("##s's:", searchable, field)

        # the fields below are not popped
        dontPopFields = {"courseid"}
        founds = Listdict()
        i = 0
        while i < len(searchable):
            found = self.getField(searchable[i], field)
            if found:
                # found a valid search condition matching the specified field
                if not (field in dontPopFields):
                    searchable.pop(i)
                    i -= 1  # step back because of the popped searchable
                founds.concat(found)
            i += 1  # next searchable
        return founds

    ##
    ## @brief      Gets rid of the empty queries in the rawQuery.
    ##
    def cleanUpRawQuery(self):
        keys = list(self.rawQuery.keys())
        for key in keys:
            value = self.rawQuery[key]
            if type(value) == list:
                self.rawQuery[key] = [elem for elem in value if elem != ""]
                value = self.rawQuery[key]
            if containsNone(value) or value == [] or value == "":
                del self.rawQuery[key]

    ##
    ## @brief      Uses the searchable to generate field of search for constructing a query.
    ##
    ## @return     None
    ##
    def parse(self):
        # converts the time into datetime format
        searchable = copy.copy(self.searchable)
        if self.length == 0:
            return None

        if self.length == 1:
            s = searchable[0]
            # it might be a course name, a course id, a room courseid,
            # (a building name),
            # or a building and room combined

            # course id
            try: self.rawQuery["courseid"] = self.getField(s, "courseid")["courseid"]
            except TypeError: pass

            # building and room combined
            _building_room = self.getField(s, "building_room")
            if _building_room:
                self.rawQuery.concat(_building_room)

            if s.isalpha():
                # might be a day
                try: self.rawQuery["day"] = self.getField(s, "day")["day"]
                except TypeError: pass
                # might be a building name
                try: self.rawQuery["building"] = self.getField(s, "building")["building"]
                except TypeError: pass
                # might be an instructor's name
                try: self.rawQuery["instructor"] = self.getField(s, "instructor")["instructor"]
                except TypeError: pass

            self.cleanUpRawQuery()
            if self.rawQuery == dict():
                self.rawQuery["rest"] = [s]

        else:
            _building_room = self.getFieldFromList(searchable, "building_room")
            if _building_room:
                self.rawQuery.concat(_building_room)
            else:
                self.rawQuery["building"] = self.getFieldFromList(searchable, "building").get("building")
                self.rawQuery["room"] = self.getFieldFromList(searchable, "room").get("room")
            self.rawQuery["courseid"] = self.getFieldFromList(searchable, "courseid").get("courseid")
            self.rawQuery["day"] = self.getFieldFromList(searchable, "day").get("day")
            self.rawQuery["rest"] = [" ".join(searchable)]

        self.cleanUpRawQuery()


##
## @brief      Gets current courses from the server.
##
## @param      current_datetime  (datetime.datetime)
## @param      time_delta        (int) The added time in minutes to find classes
##                               that are going to happen.
##
## @return     A dict with two fields: "lectures", "sections", under which are
##             lists of (coursescotty.Lecturesection) courses.
##
@LecsecFilter.filterMini(getMini())
def getCurrentCourses(current_datetime=None, time_delta=60, index=None):
    courseDict = dict()
    if current_datetime is None:
        current_datetime = datetime.datetime.now()
    shiftedDatetime = current_datetime + datetime.timedelta(minutes=time_delta)
    currentDay = current_datetime.isoweekday() % 7

    currentTimeString = current_datetime.time().strftime("%I:%M%p")
    shiftedTimeString = shiftedDatetime.time().strftime("%I:%M%p")

    QUERY_BASE = '''
    {
       "query":{
          "bool":{
             "must":{
                "match_all":{

                }
             },
             "filter":{
                "or":[
                   {
                      "nested":{
                         "inner_hits":{

                         },
                         "path":"lectures",
                         "score_mode":"avg",
                         "query":{
                            "bool":{
                               "must":
                                  {
                                     "nested":{
                                        "path":"lectures.times",
                                        "score_mode":"avg",
                                        "query":{
                                           "bool":{
                                              "filter":{
                                                 "and":[
                                                    {
                                                       "range":{
                                                          "lectures.times.end":{
                                                             "gte":"%s",
                                                             "format":"hh:mma"
                                                          }
                                                       }
                                                    },
                                                    {
                                                       "range":{
                                                          "lectures.times.begin":{
                                                             "lte":"%s",
                                                             "format":"hh:mma"
                                                          }
                                                       }
                                                    }
                                                 ]
                                              }
                                           }
                                        }
                                     }
                                  }

                            }
                         }
                      }
                   },
                   {
                      "nested":{
                         "inner_hits":{

                         },
                         "path":"sections",
                         "score_mode":"avg",
                         "query":{
                            "bool":{
                               "must":
                                  {
                                     "nested":{
                                        "path":"sections.times",
                                        "score_mode":"avg",
                                        "query":{
                                           "bool":{
                                              "filter":{
                                                 "and":[
                                                    {
                                                       "range":{
                                                          "sections.times.end":{
                                                             "gte":"%s",
                                                             "format":"hh:mma"
                                                          }
                                                       }
                                                    },
                                                    {
                                                       "range":{
                                                          "sections.times.begin":{
                                                             "lte":"%s",
                                                             "format":"hh:mma"
                                                          }
                                                       }
                                                    }
                                                 ]
                                              }
                                           }
                                        }
                                     }
                                  }

                            }
                         }
                      }
                   }
                ]
             }
          }
       }
    }
    '''

    queryString = QUERY_BASE % (currentTimeString, shiftedTimeString, currentTimeString, shiftedTimeString)
    query = json.loads(queryString)

    for i in [0, 1]:
        query["query"]["bool"]["filter"]["or"][i]\
             ["nested"]["query"]["bool"]["must"]\
             ["nested"]["query"]["bool"]["must"] = []

    query["query"]["bool"]["filter"]["or"][0]\
         ["nested"]["query"]["bool"]["must"]\
         ["nested"]["query"]["bool"]["must"].append(
            {"match": {"lectures.times.days": currentDay}})
    query["query"]["bool"]["filter"]["or"][1]\
         ["nested"]["query"]["bool"]["must"]\
         ["nested"]["query"]["bool"]["must"].append(
            {"match": {"sections.times.days": currentDay}})

    response = queryCourse(query, index=index)

    if "hits" in response:
        courseDict = parseResponse(response)
    return courseDict


def presearch(search_text):
    result = dict()
    match = re.search("15112|15-112|kosbie|koz", search_text)
    if match:
        result["mainpage_toast"] = random.choice(cmu_info.ONETWELVE)
    return result


def search(text=None, index=None):
    if text is not None:
        searcher = Searcher(text)
        query = searcher.generateQuery()
        response = queryCourse(query, index=index)
        rawQuery = searcher.rawQuery

        if "hits" in response:
            result = parseResponse(response)
            result["raw_query"] = rawQuery
            return result


##
## @brief      Get the course by courseid.
##
## @param      courseid  (str) The courseid
## @param      index     (str) The elasticsearch index
##
## @return     A dictionary
#              {course: <coursescotty.Course object containing the course info>,
#               response: <response from the server>
#              }
#
def getCourseByID(courseid, index=None):
    output = {'response': {},
              'course': None}
    if index is None:
        index = ALL_COURSES_INDEX
    if re.search("^\d\d-\d\d\d$", courseid):
        searcher = Searcher(courseid)
        query = searcher.generateQuery()
        response = queryCourse(query, index=index)

        output['response'] = response
        if response.get("status") is not None:
            return output
        if "hits" in response and response['hits']['hits'] != []:
            output['course'] = Course(response['hits']['hits'][0]['_source'])
    return output


def queryCourse(query, index=None):
    if index is None:
        index = getCurrentIndex()
    servers = ['courseapi-scotty.rhcloud.com:80']
    response = fetch(index, query, servers)
    return response


def fetch(index, query, servers, size=200):
    es = Elasticsearch(servers)
    response = dict()
    try:
        response = es.search(
            index = index,
            body = query,
            size = size
        )
    except elasticsearch.exceptions.NotFoundError as e:
        print(formatErrMsg(e, "ES"))
        response = e.info
    except elasticsearch.exceptions.RequestError as e:
        print(formatErrMsg(e, "ES"))
        response = e.info
    except elasticsearch.exceptions.TransportError as e:
        print(formatErrMsg(e, "ES"))
        response = e.info

    # except:
    #     pass

    return response


@LecsecFilter.filterPittsburgh
def parseResponse(response):
    # The switch for filtering based on inner hits
    shouldFilter = True
    courseDict = {
        "lectures": [],
        "sections": []
    }
    if "hits" in response and response['hits']['hits'] != []:
        for hit in response['hits']['hits']:
            d = Course(hit['_source']).split()

            hitLectures = None
            hitSections = None

            try: hitLectures = hit["inner_hits"]["lectures"]["hits"]["hits"]
            except: pass
            try: hitSections = hit["inner_hits"]["sections"]["hits"]["hits"]
            except: pass

            if shouldFilter and hitLectures is not None:
                courseDict["lectures"] += filterWithInnerHits(d["lectures"], hitLectures)
            else:
                courseDict["lectures"] += d["lectures"]

            if shouldFilter and hitSections is not None:
                courseDict["sections"] += filterWithInnerHits(d["sections"], hitSections)
            else:
                courseDict["sections"] += d["sections"]

    return courseDict


def filterWithInnerHits(events, innerhits_hits_hits):
    names = [hit['_source']['name'] for hit in innerhits_hits_hits]
    names = set(names)
    # print(innerhits_hits_hits)
    filteredEvents = []
    for event in events:
        # print(event.lecsec)
        if event.lecsec in names:
            filteredEvents.append(event)
    return filteredEvents
