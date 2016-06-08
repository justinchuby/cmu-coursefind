import datetime
import re
import copy
import random

import json, urllib
from http import client as Client

try:
    from . import cmu_info
    from .utilities import *
except:
    import cmu_info
    from utilities import *


from elasticsearch import Elasticsearch

# class Server():
#     def __init__(self, address, port):
#         self.address = address
#         self.port = port

##
## @brief      Checks if there is a None in a list/tuple/set/dict.
##
## @param      thing
##
## @return     bool
##
def containsNone(thing):
    if thing is None:
        return True
    if isinstance(thing, str):
        return False
    if ((isinstance(thing, list) or isinstance(thing, tuple)
        or isinstance(thing, set) or isinstance(thing, dict)) and None in thing):
        return True
    return False


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
    def __init__(self, s="", looseField=None):
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
            self.rawQuery["building_room"] = self.getField(s, "building_room")

            if s.isalpha():
                # might be a day
                self.rawQuery["day"] = self.getField(s, "day")
                # might be a building name
                self.rawQuery["building"] = self.getField(s, "building")
                if not self.rawQuery["day"] and not self.rawQuery["building"]:
                    self.rawQuery["rest"] = s

        else:
            self.rawQuery["number"] = self.getFieldFromList(searchable, "number")
            (self.rawQuery["building"], self.rawQuery["room"]) = self.getFieldFromList(searchable, "building_room")
            if self.rawQuery["room"] is None:
                self.rawQuery["building"] = self.getFieldFromList(searchable, "building")

            self.rawQuery["day"] = self.getFieldFromList(searchable, "day")
            self.rawQuery["rest"] = searchable.join(" ")

        self.cleanUpRawQuery()

    ##
    ## @brief      Generate the query for the database.
    ## 
    ## @return     (dict) The query for querying the database.
    ##
    def generateQuery(self):
        return self.constructESQueryFromRaw(self.rawQuery)

    @staticmethod
    def constructESQueryFromRaw(rawQuery):
        print(rawQuery)
        # Filtering fields are not in the query
        if (("day" not in rawQuery) and ("building" not in rawQuery) and
            ("room" not in rawQuery) and ("number" not in rawQuery)):
            query = {
                "query": { 
                  "query_string" : {
                     "query" : rawQuery["rest"]
                  }
                }
            }

        else:
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
                           }
                        ]
                     }
                  }
               }
            }
            '''

            query = json.loads(QUERY_BASE)

            # fields: building, building_room, number, time
            if "day" in rawQuery:
                query["query"]["bool"]["filter"]["or"][0]\
                     ["nested"]["query"]["bool"]["must"]\
                     ["nested"]["query"]["bool"]["must"].append(
                        {"match": {"lectures.times.days": rawQuery["day"]}})
                query["query"]["bool"]["filter"]["or"][1]\
                     ["nested"]["query"]["bool"]["must"]\
                     ["nested"]["query"]["bool"]["must"].append(
                        {"match": {"sections.times.days": rawQuery["day"]}})

            if "building" in rawQuery:
                query["query"]["bool"]["filter"]["or"][0]\
                     ["nested"]["query"]["bool"]["must"]\
                     ["nested"]["query"]["bool"]["must"].append(
                        {"match": {"lectures.times.building": rawQuery["building"]}})
                query["query"]["bool"]["filter"]["or"][1]\
                     ["nested"]["query"]["bool"]["must"]\
                     ["nested"]["query"]["bool"]["must"].append(
                        {"match": {"sections.times.building": rawQuery["building"]}})

            if "room" in rawQuery:
                query["query"]["bool"]["filter"]["or"][0]\
                     ["nested"]["query"]["bool"]["must"]\
                     ["nested"]["query"]["bool"]["must"].append(
                        {"match": {"lectures.times.room": rawQuery["room"]}})
                query["query"]["bool"]["filter"]["or"][1]\
                     ["nested"]["query"]["bool"]["must"]\
                     ["nested"]["query"]["bool"]["must"].append(
                        {"match": {"sections.times.room": rawQuery["room"]}})

            if "number" in rawQuery:
                query["query"]["bool"]["must"] = {"term": {"id": rawQuery["number"]}}
                if (("day" not in rawQuery) and ("building" not in rawQuery) and
                    ("room" not in rawQuery)):
                    del query["query"]["bool"]["filter"]
            elif "rest" in rawQuery:
                query["query"]["query_string"] = {"query": rawQuery["rest"]}
            else:
                query["query"]["bool"]["must"] = {"match_all": {}}

        return query


def search(text):
    searcher = Searcher(text)
    query = searcher.generateQuery()
    index = "test7"
    servers = ["courseapi-scotty.rhcloud.com:80"]
    response = fetch(index, query, servers)
    for hit in response['hits']['hits']:
        print(hit['_source'])


def fetch(index, query, servers):
    es = Elasticsearch(servers)
    response = es.search(
        index = index,
        body = query,
        size = 20
        )
    return response

