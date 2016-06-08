# @file coursescotty.py
# @brief Contains the Event, Course etc. classes.
# @author Justin Chu (justinchuby@cmu.edu)


import re
import datetime

try:
    from utilities import *
except:
    from .utilities import *


class Course(object):
    def __init__(self, scotty_dict):
        self.courseid = scotty_dict["id"]
        self.scottyDict = copy.deepcopy(scotty_dict)
        self.lectures = self.scottyDict["lectures"]
        self.sections = self.scottyDict["sections"]

    def __repr__(self):
        s = ""
        for key, item in self.scottyDict.items():
            s += "{}: {}\n".format(repr(key), repr(item))
        s = "</Course: " + s + "/>"
        return s

    ##
    ## @brief      Get lists of lectures and sections in a dictionary.
    ##
    ## @param      self  The Course object.
    ##
    ## @return     A dictionary of two lists.
    ##
    def split(self):
        output = {
            "lectures": [],
            "sections": []
        }

        baseInfo = copy.copy(self.scottyDict)
        baseInfo["number"] = baseInfo["id"]
        del baseInfo["lectures"]
        del baseInfo["sections"]

        _KEYS = ["lectures", "sections"]
        for key in _KEYS:
            if self.__dict__[key] != []:
                for lecsecDict in self.__dict__[key]:
                    _baseInfo = copy.deepcopy(baseInfo)

                    # Add type
                    if key == "lectures":
                        _baseInfo["type"] = "lec"
                    elif key == "sections":
                        _baseInfo["type"] = "sec"

                    # Pull up the lecture/section object one level
                    for field in lecsecDict:
                        if field == "name":
                            _baseInfo["lecsec"] = lecsecDict[field]
                        else:
                            _baseInfo[field] = lecsecDict[field]
                    output[key].append(LectureSection(_baseInfo))
        return output


class LectureSection(object):
    def __init__(self, reduced_scotty_dict):
        self.KEYS = ["number", "name", "units", "lecsec", "times", "instructors",
                     "rundate", "department", "coreqs", "prereqs", "type"]
        for key in self.KEYS:
            self.__dict__[key] = copy.deepcopy(reduced_scotty_dict[key])

    def __repr__(self):
        s = ""
        for key in self.KEYS:
            s += "{}: {}, ".format(repr(key), repr(self.__dict__[key]))
        s = "</LectureSection: " + s + "/>"
        return s

    def update(self, reduced_scotty_dict):
        self.__init__(reduced_scotty_dict)



##
## @brief      A list that contains the events.
##
class CourseList(list):
    def __init__(self, L=None):
        if L is None:
            L = []
        super().__init__(L)
        self.past = []
        self.current = []
        self.future = []
        self.rest = []
        self.laterToday = []
        self.len = 0
        self.ready()

    ##
    ## @brief      Places the course objects into different lists.
    ##
    ## @param      self             Self
    ## @param      currentDatetime  (datetime.datetime)  Specify the current
    ##                              date and time
    ## @param      timeDelta        (int)  the time to define 'future' events
    ##
    ## @return     None
    ##
    def ready(self, currentDatetime=None, timeDelta=60):
        self.len = self.__len__()
        self.past = []
        self.current = []
        self.future = []
        self.rest = []
        self.laterToday = []
        _dateTime = datetime.datetime(2015,1,1)

        if not isinstance(currentDatetime, datetime.datetime):
            currentDatetime = datetime.datetime.now()
        currentTime = currentDatetime.time()
        currentDay = str(currentDatetime.isoweekday() % 7)

        for event in self:
            for time in event.times
            # add attribute to event for diaplay
            event.days_text = getDaysText(event.days)
            event.building_text = getBuildingText(event.building)

            if currentDay in event.times:
                # ended event
                if event.endTime < currentTime:
                    event.diffText = "{}:{}".format(event.beginTime.hour, event.beginTime.minute)
                    self.past.append(event)
                # current event
                elif event.beginTime < currentTime < event.endTime:
                    diff = getTimeDifference(event, "current", currentDatetime)
                    _time = _dateTime + diff
                    if diff.seconds <= 3600:
                        event.diffText = "Ends in {} minutes".format(_time.minute)
                    else:
                        event.diffText = "Ends in {} h {} minutes".format(_time.hour, _time.minute)
                    self.current.append(event)
                # future event (in timeDelta minutes)
                elif (event.beginTime > currentTime and
                        event.intBeginTime < inMinutes(currentTime) + timeDelta):
                    diff = getTimeDifference(event, "future", currentDatetime)
                    _time = _dateTime + diff
                    if diff.seconds <= 3600:
                        event.diffText = "Begins in {} minutes".format(_time.minute)
                    else:
                        event.diffText = "Begins in {} h {} minutes".format(_time.hour, _time.minute)
                    self.future.append(event)
                # other
                else:
                    event.diffText = "{}:{}".format(event.beginTime.hour, event.beginTime.minute)
                    self.laterToday.append(event)
            else:
                event.diffText = event.days_text
                self.rest.append(event)


    def sortByTime(self, currentDatetime=None):
        self.ready(currentDatetime)
        return self.current + self.future + self.laterToday + self.past + self.rest
        
