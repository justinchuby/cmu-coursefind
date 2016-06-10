import datetime
import re
import copy

import json

try:
    from . import cmu_info
    from .utilities import *
    from .coursescotty import *
except:
    import cmu_info
    from utilities import *
    from coursescotty import *


from elasticsearch import Elasticsearch
import elasticsearch


##
## @brief      Defines a Searcher object.
##
class Searcher(object):

    ##
    ## @brief      init
    ##
    ## @param      self        
    ## @param      s           The query text
    ##
    def __init__(self, s=""):
        self.text = s.strip()
        self.rawQuery = dict()
        self.searchable = splitString(self.text.lower(), " ")
        self.length = len(self.searchable)

        self.parseSearchBox()

    def __repr__(self):
        return str(self.rawQuery)

    ##
    ## @brief      Constructs the query for a given field.
    ##
    ## @param      s      (str) Input text
    ## @param      field  (str) The specified field type
    ##
    ## @return     Depends on the field type. List or tuple for multiple
    ##             outputs, string for a single output, None if nothing.
    ##
    @staticmethod
    def getField(s, field):
# DEBUG
        print("##s:", s, field)
        # Match course id in forms of "36217" or "36-217"
        if field == "number":
            if s.isdigit() and len(s) == 5:
                return s[:2] + "-" + s[2:]
            else:
                match = re.search("\d\d-\d\d\d", s)
                if match:
                    return match.group()
            return None
        # Match building in forms of "BH136A"
        if field == "building_room":
            match = re.search("^([a-zA-Z][a-zA-Z]+)(\d+\w*)", s)
            if match:
                return (match.group(1).upper(), match.group(2).upper())
            return (None, None)

        if field == "building":
            if s in cmu_info.CMU_BUILDINGS:
                return cmu_info.CMU_BUILDINGS[s]
            elif s in cmu_info.CMU_BUILDINGS_ABBR:
                return s.upper()
            return None

        if field == "day":
            if s in cmu_info.DAYS_STRING:
                return cmu_info.DAYS_STRING[s]
            return None

    ##
    ## @brief      Gets the query for a specified from the searchable list
    ##
    ## @param      self
    ## @param      searchable  The searchable list consists of strings as elements
    ## @param      field       The specified field
    ## @param      multiple    Whether or not to look for multiple results
    ##
    ## @return     A query string for the field if multiple is False; a list of query strings if multiple is Ture.
    ##
    def getFieldFromList(self, searchable, field):
# DEBUG
        print("##s's:", searchable, field)
        # the fields below are not popped
        dontPopFields = {}
        i = 0
        while i < len(searchable):
            found = self.getField(searchable[i], field)
            if not containsNone(found):
                # found a valid search condition
                if not (field in dontPopFields):
                    searchable.pop(i)
                    i -= 1  # step back because of the popped searchable
                # if multiple:
                #     founds.append(found)
                # else:
                return found
            i += 1  # next searchable
        return found


    ##
    ## @brief      Gets rid of the empty queries in the rawQuery.
    ##
    def cleanUpRawQuery(self):
        d = copy.copy(self.rawQuery)
        for key, value in d.items():
            if containsNone(value) or value == [] or value == "":
                del self.rawQuery[key]


    ##
    ## @brief      Uses the searchable to generate field of search for constructing a query.
    ## 
    ## @return     None
    ##
    def parseSearchBox(self):
        # converts the time into datetime format
        searchable = copy.copy(self.searchable)
        if self.length == 0:
            return None

        if self.length == 1:
            s = searchable[0]
            # it might be a course name, a course number, a room number,
            # (a building name),
            # or a building and room combined

            # course number
            self.rawQuery["number"] = self.getField(s, "number")

            # building and room combined
            (self.rawQuery["building"], self.rawQuery["room"]) = self.getField(s, "building_room")

            if s.isalpha():
                # might be a day
                self.rawQuery["day"] = self.getField(s, "day")
                # might be a building name
                self.rawQuery["building"] = self.getField(s, "building")
# TODO: This doesn't look good
            self.cleanUpRawQuery()
            if self.rawQuery == dict():
                self.rawQuery["rest"] = s

        else:
            (self.rawQuery["building"], self.rawQuery["room"]) = self.getFieldFromList(searchable, "building_room")
            if self.rawQuery["room"] is None:
                self.rawQuery["building"] = self.getFieldFromList(searchable, "building")

            self.rawQuery["day"] = self.getFieldFromList(searchable, "day")
            self.rawQuery["rest"] = " ".join(searchable)

        self.cleanUpRawQuery()

    ##
    ## @brief      Generate the query for the database.
    ## 
    ## @return     (dict) The query for querying the database.
    ##
    def generateQuery(self):
        return self.constructESQueryFromRaw(self.rawQuery)

    @staticmethod
    def constructESQueryFromRaw(raw_query):
        print(raw_query)
        # Filtering fields are not in the query

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

        query["query"]["bool"]["filter"]["or"][0]\
             ["nested"]["query"]["bool"]["must"]\
             ["nested"]["query"]["bool"]["must"].append(
                {"match": {"lectures.times.location": "Pittsburgh, Pennsylvania"}})
        query["query"]["bool"]["filter"]["or"][1]\
             ["nested"]["query"]["bool"]["must"]\
             ["nested"]["query"]["bool"]["must"].append(
                {"match": {"sections.times.location": "Pittsburgh, Pennsylvania"}})


        if (("day" not in raw_query) and ("building" not in raw_query) and
            ("room" not in raw_query) and ("number" not in raw_query)):
            query["query"]["query_string"] = {
                "query" : raw_query["rest"]
            }
        else:
            # fields: building, building_room, number, time
            if "day" in raw_query:
                query["query"]["bool"]["filter"]["or"][0]\
                     ["nested"]["query"]["bool"]["must"]\
                     ["nested"]["query"]["bool"]["must"].append(
                        {"match": {"lectures.times.days": raw_query["day"]}})
                query["query"]["bool"]["filter"]["or"][1]\
                     ["nested"]["query"]["bool"]["must"]\
                     ["nested"]["query"]["bool"]["must"].append(
                        {"match": {"sections.times.days": raw_query["day"]}})

            if "building" in raw_query:
                query["query"]["bool"]["filter"]["or"][0]\
                     ["nested"]["query"]["bool"]["must"]\
                     ["nested"]["query"]["bool"]["must"].append(
                        {"match": {"lectures.times.building": raw_query["building"]}})
                query["query"]["bool"]["filter"]["or"][1]\
                     ["nested"]["query"]["bool"]["must"]\
                     ["nested"]["query"]["bool"]["must"].append(
                        {"match": {"sections.times.building": raw_query["building"]}})

            if "room" in raw_query:
                query["query"]["bool"]["filter"]["or"][0]\
                     ["nested"]["query"]["bool"]["must"]\
                     ["nested"]["query"]["bool"]["must"].append(
                        {"match": {"lectures.times.room": raw_query["room"]}})
                query["query"]["bool"]["filter"]["or"][1]\
                     ["nested"]["query"]["bool"]["must"]\
                     ["nested"]["query"]["bool"]["must"].append(
                        {"match": {"sections.times.room": raw_query["room"]}})

            if "number" in raw_query:
                query["query"]["bool"]["must"] = {"term": {"id": raw_query["number"]}}
                if (("day" not in raw_query) and ("building" not in raw_query) and
                    ("room" not in raw_query)):
                    del query["query"]["bool"]["filter"]
            elif "rest" in raw_query:
                query["query"]["query_string"] = {"query": raw_query["rest"]}
            else:
                query["query"]["bool"]["must"] = {"match_all": {}}

        return query


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
def getCurrentCourses(current_datetime=None, time_delta=60):
    if current_datetime is None:
        current_datetime = datetime.datetime.now()
    shiftedDatetime = current_datetime + datetime.timedelta(minutes=time_delta)
    currentDay = current_datetime.isoweekday() % 7
    time = inMinutes(currentTime)

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
                               "must":[
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
                                                             "gte":"{0}"},
                                                             "format":"hh:mma"
                                                          }
                                                       }
                                                    },
                                                    {
                                                       "range":{
                                                          "lectures.times.begin":{
                                                             "lte":"{0}"},
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
                               ]
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
                               "must":[
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
                                                             {"gte":"{1}"},
                                                             "format":"hh:mma"
                                                          }
                                                       }
                                                    },
                                                    {
                                                       "range":{
                                                          "sections.times.begin":{
                                                             "lte":"{1}}",
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
                               ]
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
    
    queryString = QUERY_BASE.format(shiftedDatetime.time().strftime("%I:%M%p"),
                                    current_datetime.time().strftime("%I:%M%p"))
    query = {
             "intBeginTime": {"$lt": time + time_delta},
             "intEndTime": {"$gt": time},
             "city_searchable": {"$all": ["pittsburgh"]},
             "days_searchable": str(currentDay)
            }

    courses = fetchCourse(query)

    return courses


def presearch(search_text):
    # returns shouldSearch, message
    search_text = " ".join(getSearchable(search_text))

    match = re.search("15112|112|kosbie|kos", search_text)
    if match:
        return True, random.choice(cmu_info.ONETWELVE)
    return True, None


def search(text):
    searcher = Searcher(text)
    query = searcher.generateQuery()
    index = getCurrentIndex()
    servers = ["courseapi-scotty.rhcloud.com:80"]
    response = fetch(index, query, servers)
 
    if "hits" in response:
        return parseResponse(response)
    else:
        return None


def getCurrentIndex():
    # currentYear = datetime.date.today().year
    # currentMonth = datetime.date.today().month
    # return getIndex(currentYear, currentMonth)
    return "test9"


def getIndex(year, month):
    if 1 <= month <= 4:
        semester = "s"
    elif 5 <= month <= 6:
        semester = "m1"
    elif month == 7:
        semester = "m2"
    else:
        semester = "f"
    index = semester + str(year)[2:]
    return index


def fetch(index, query, servers):
    es = Elasticsearch(servers)
    response = dict()
    try:
        response = es.search(
            index = index,
            body = query,
            size = 2
        )
    except elasticsearch.exceptions.NotFoundError:
        print("'index_not_found_exception', 'no such index'")
    return response


def parseResponse(response):
    courseDict = {
        "lectures": [],
        "sections": []
    }
    if "hits" in response and response['hits']['hits'] != []:
        for hit in response['hits']['hits']:
                d = Course(hit['_source']).split()
                courseDict["lectures"] += d["lectures"]
                courseDict["sections"] += d["sections"]
    return courseDict

