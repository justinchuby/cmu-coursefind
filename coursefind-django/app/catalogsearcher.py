# the fetch() function is adapted from https://parse.com/docs/rest/guide

import datetime
import re
import copy
import random

import json, urllib
from http import client as Client

try:
    from . import coursecat, cmu_info, cmu_prof
    from .utilities import *
except:
    import coursecat, cmu_info, cmu_prof
    from utilities import *

DAYS_STRING = {"monday": "0",
               "tuesday": "1",
               "wednesday": "2",
               "thursday": "3",
               "friday": "4",
               "saturday": "5",
               "sunday": "6",
               "mon": "0",
               "tue": "1",
               "wed": "2",
               "thu": "3",
               "fri": "4",
               "sat": "5",
               "sun": "6"}

def containsNone(thing):
    if thing is None:
        return True
    if isinstance(thing, str):
        return False
    if ((isinstance(thing, list) or isinstance(thing, tuple)
        or isinstance(thing, set) or isinstance(thing, dict)) and None in thing):
        return True

    return False

class Searcher(object):

    def __init__(self, s="", looseField=None):
        self.text = s.strip()
        self.rawQuery = dict()
        self.looseField = looseField
        self.searchable = coursecat.getSearchable(self.text)
        if len(self.searchable) > 20:
            self.searchable = self.searchable[:20]
        self.length = len(self.searchable)

        self.parseSearchBox()

    def __repr__(self):
        return str(self.rawQuery)

    @staticmethod
    def getField(s, field):
        if field == "number":
            if s.isdigit():
                if len(s) == 3:
                    return [s]
                if len(s) == 5:
                    return [s[:2], s[2:]]
            return None
        if field == "building_room":
            match = re.search("^([a-zA-Z][a-zA-Z]+)(\d+\w*)", s)
            if match:
                return (match.group(1).upper(), match.group(2).upper())
            return (None, None)
        if field == "room":
            if s.isdigit() and len(s) > 4:
                return None
            match = re.search("^([a-zA-Z]?\d+\w*)", s)
            if match:
                return match.group(1).upper()
            return None

        if field == "building":
            if s in cmu_info.CMU_BUILDINGS:
                return cmu_info.CMU_BUILDINGS[s]
            elif s in cmu_info.CMU_BUILDINGS_ABBR:
                return s.upper()
            return None

        if field == "days":
            if s in DAYS_STRING:
                return DAYS_STRING[s]
            return None

        if field == "instructor":
            # see if the string is a part of the name of a instructor
            # could be first name or last name or both
            if s in cmu_prof.NAMES:
                return s
            return None


    def getFieldFromList(self, searchable, field, multiple=False):
        # the fields below are not popped
        dontPopFields = {"number"}
        i = 0
        founds = []
        while i < len(searchable):
            found = self.getField(searchable[i], field)
            if not containsNone(found):
                # found a valid search condition
                if not (field in dontPopFields or
                   (field == "room" and found.isdigit())):
                    searchable.pop(i)
                    i -= 1  # step back because of the popped searchable
                if multiple:
                    founds.append(found)
                else:
                    return found
            i += 1  # next searchable
        if multiple:
            return founds
        else:
            return found

    def cleanUpRawQuery(self):
        d = copy.copy(self.rawQuery)
        for key, value in d.items():
            if containsNone(value) or value == [] or value == "":
                del self.rawQuery[key]

    def parseSearchBox(self):
        # takes in a string and returns field of search for constructing a query
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
            self.rawQuery["building"], self.rawQuery["room"] = self.getField(s, "building_room")
            if self.rawQuery["room"] is None:
                # just room number
                #   digit followed by (probably) letters
                #   or one letter follow by digits (probably) letters
                self.rawQuery["room"] = self.getField(s, "room")

            if s.isalpha():
                # might be a day
                self.rawQuery["days"] = self.getField(s, "days")
                # might be a building name
                self.rawQuery["building"] = self.getField(s, "building")
                if self.rawQuery["days"] is None and self.rawQuery["building"] is None:
                    # add the instructor field in case if the name is not in the prof list
                    self.rawQuery["instructor_unknown"] = searchable
                    # the rest might be a part of a course name
                    self.rawQuery["name_searchable"] = searchable

        # elif self.length == 2:
        #     # first consider (PH 100) type of things
        #     building = self.getField(searchable[0], "building")
        #     room = self.getField(searchable[1], "room")
        #     if building is not None and room is not None:
        #         self.rawQuery["building"] = building
        #         self.rawQuery["room"] = room
        #         self.rawQuery["day"] = self.getFieldFromList(searchable, "days")
        #     else:
        #         self.rawQuery["name_searchable"] = searchable
        #         self.rawQuery["instructor"] = searchable

        else:
            # if self.length == 2:
            #     # check if it's a professor's full name
            #     self.rawQuery["instructor_known"] = []
            #     if " ".join(self.searchable) in cmu_prof.FULL_NAMES:
            #         self.rawQuery["instructor_known"] = self.searchable

            # if self.length > 2 or len(self.rawQuery["instructor_known"]) < 2:
            self.rawQuery["number"] = self.getFieldFromList(searchable, "number")
            (building, room) = self.getFieldFromList(searchable, "building_room")
            if building is not None:
                self.rawQuery["building"] = building
                self.rawQuery["b_room"] = room
                # b_room: building determined room
            else:
                self.rawQuery["building"] = self.getFieldFromList(searchable, "building")
            if room is None:
                room = self.getFieldFromList(searchable, "room")
                if room is not None and not room.isdigit():
                    self.rawQuery["b_room"] = room
                else:
                    self.rawQuery["room"] = room

            self.rawQuery["days"] = self.getFieldFromList(searchable, "days")

            self.rawQuery["instructor_known"] = self.getFieldFromList(searchable, "instructor", multiple=True)

            # get rid of numbers
            searchableSet = set(searchable)
# DEBUG
            # print(searchable)
            # print(searchableSet)
            for elem in searchable:
                if elem.isdigit():
                    searchableSet.discard(elem)
# DEBUG
                    # print(elem, "!")
            searchable = list(searchableSet)

            # the string left is a course name or a prof's name
            # add the instructor field in case if the name is not in the prof list
            self.rawQuery["instructor_unknown"] = searchable
            self.rawQuery["name_searchable"] = searchable

        self.rawQuery["city"] = ["pittsburgh"]
        self.cleanUpRawQuery()

    def generateQuery(self, service="parse"):
        return self.generateQueryFromRaw(self.rawQuery, service, self.looseField)

    @staticmethod
    def generateQueryFromRaw(rawQuery, service="parse", looseField=None):
        if looseField is None:
            looseField = set()
        query = dict()
        # generate query from a dict with parsed search fields
        # try different combination of search fields

        if service == "parse":
            # fill in other constrains
            query["$or"] = []
            # fields: building, room, name, number, time, prof, location
            if "days" in rawQuery:
                query["days_searchable"] = rawQuery["days"]
            # elif "building" in rawQuery:
            #     # if only searching for a room
            #     query["days_searchable"] = str(datetime.datetime.now().weekday())

            # if "time" in rawQuery:
            #     time = inMinutes(rawQuery["time"])
            #     query["intBeginTime"] = {"$lt": time}
            #     query["intEndTime"] = {"$gt": time}

            if "building" in rawQuery:
                query["building"] = rawQuery["building"]

            if "b_room" in rawQuery:
                query["room"] = rawQuery["b_room"]

            elif "room" in rawQuery:
                # query["room"] = rawQuery["room"]
                query["$or"].append({"room": 
                                        rawQuery["room"]
                                    })


            if "name_searchable" in rawQuery:
                if "name" in looseField:
                    for name in rawQuery["name_searchable"]:
                        query["$or"].append({"name_searchable": name })
                else:
                    query["$or"].append({"name_searchable": {
                                            "$all": rawQuery["name_searchable"]
                                        }})


            # if "instructor" in rawQuery:
            #     for i in range(len(rawQuery["instructor"])):
            #         query["$or"].append({"instructor_searchable": 
            #                                 rawQuery["instructor"][i]
            #                             })

            # query["instructor_searchable"] = {"$all": []}

            # first check if it is a recorded instructor
            if "instructor_known" in rawQuery:
                instructors = rawQuery["instructor_known"]
                query["instructor_searchable"] = {"$all": instructors}

            # otherwise it might be a not recorded instructor
            elif "instructor_unknown" in rawQuery:
                for i in range(len(rawQuery["instructor_unknown"])):
                    query["$or"].append({"instructor_searchable": 
                                            rawQuery["instructor_unknown"][i]
                                        })

            if "city" in rawQuery:
                query["city_searchable"] = {"$all": rawQuery["city"]}

            if "number" in rawQuery:
                if "room" not in rawQuery:
                    # if room is not in query, the number is determined
                    query["number_searchable"] = {"$all": rawQuery["number"]}
                else:
                    # if room is in query, number is not determined
                    # query["number_searchable"] = {"$all": d["number"]}
                    query["$or"].append({"number_searchable": {
                                            "$all": rawQuery["number"]
                                        }})

            # delete the $or query if it is empty
            if query["$or"] == []:
                del query["$or"]
        return query

    def printJSONQuery(self):
        jsonQuery = json.dumps(self.generateQuery(), sort_keys=True, indent=4)

def getCurrentCourses(timeDelta=60, currentDatetime=None):
    if currentDatetime is None:
        currentDatetime = datetime.datetime.now()
    currentTime = currentDatetime.time()
    currentDay = currentDatetime.weekday()
    time = inMinutes(currentTime)

    query = {
             "intBeginTime": {"$lt": time + timeDelta},
             "intEndTime": {"$gt": time},
             "city_searchable": {"$all": ["pittsburgh"]},
             "days_searchable": str(currentDay)
            }

    courses = fetchCourse(query)

    return courses


def presearch(searchText):
    # returns shouldSearch, message
    searchText = " ".join(getSearchable(searchText))

    match = re.search("15112|112|kosbie|kos", searchText)
    if match:
        return True, random.choice(cmu_info.ONETWELVE)
    return True, None


def search(searchText, looseField=None):
    searcher = Searcher(searchText)
    courses = []
    query = dict()
    if looseField is None:
        query = searcher.generateQuery()

    elif "name" in looseField and "name_searchable" in searcher.rawQuery:
        newSearcher = Searcher(searchText, looseField)
        query = newSearcher.generateQuery()
# DEBUG
    print(json.dumps(query, sort_keys=True, indent=4))
    if query != {}:
        courses = fetchCourse(query)

    # if courses == []:
    #     return None
    return courses


def filter(course, condition):
    return 42


def fetchCourse(query):
    table = '/classes/CMU_catalog_2016_spring'
    try:
        return parseJSONToCourses(fetch(query, table))
    except:
# DEBUG
        print("unable to get courses")
        return []


def fetch(query, table):
    # limits items retrieve
    limit = 250
    connection = Client.HTTPSConnection('api.parse.com', 443)
    params = urllib.parse.urlencode({"where": json.dumps(query), "limit": limit})

    connection.connect()
    connection.request('GET', '/1{}?{}'.format(table, params), '', {
           "X-Parse-Application-Id": "aPrDGVlJf7yoRnoTx1uUyWSYotyrpofeDd3Nu7kA",
           "X-Parse-REST-API-Key": "fF1kG1pVvFajVmABdvDh4YEAkBjCvyzOscz0uZO4"
         })
    result = connection.getresponse().read().decode()
    return result


def parseJSONToCourses(JSONMessage):
    result = json.loads(JSONMessage)
    results = result.get("results", result)
    courses = []
    if "error" in result:
# DEBUG
        print(result)
        return []
    else:
        for elem in results:
            courses.append(coursecat.Course(elem))
    return courses


#########################################################

def test_containsNone():
    assert(containsNone(['21', '127']) is False)
    assert(containsNone(None) is True)
    assert(containsNone([None, None]) is True)
    assert(containsNone(['None', 'None']) is False)
    assert(containsNone((None, None)) is True)
    assert(containsNone(([None, None])) is True)

def test_dayFilter():
    currentDatetime = datetime.datetime.now()
    currentDay = str(currentDatetime.weekday())
    print("today is", currentDay)

    query = {
             "days": {"$regex": "\d*" + currentDay + "\d*"},
             # "city": "Pittsburgh, Pennsylvania",
             # "name": "Naval Laboratory",
            }

    courses = fetchCourse(query)
    print("there are {} courses".format(len(courses)))
    for course in courses:
        print(course)


def test_getCurrentCourses():
    # # courses = catalogparser.parseSOC("Course_Catalog/SOC_S16.html")
    # print("reading...")
    # # courses = catalogparser.parseSOC("Course_Catalog/Carnegie Mellon 
    # # University - Full Schedule Of Classes.html")
    # print("reading done\n")

    currentDatetime = datetime.datetime.now()
    currentDate = currentDatetime.date()

    print("It is now", currentDatetime)
    currentCourses = getCurrentCourses()
    print("There are {} courses happening".format(len(currentCourses)))
    currentCourses.sort(key=lambda x: (x.building, x.room))
    result = ""
    for course in currentCourses:
        diff = datetime.datetime.combine(currentDate, course.endTime) - currentDatetime
        diff = inMinutes(diff)
        result += "{} {} / {} {}\n".format(course.building, course.room,
                                           course.number, course.name)
        result += "ends in {} minutes\n".format(str(diff))
    print(result)
