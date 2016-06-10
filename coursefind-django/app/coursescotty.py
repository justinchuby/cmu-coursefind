# @file coursescotty.py
# @brief Contains the Event, Course etc. classes.
# @author Justin Chu (justinchuby@cmu.edu)


import datetime
import copy

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
## @brief      A list that contains the courses.
##
class CourseList(list):
    def __init__(self, L=None):
        if L is None:
            L = []
        super().__init__(L)
        self.past = []
        self.current = []
        self.laterToday = []
        self.future = []
        self.rest = []
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
    def ready(self, current_datetime=None, time_delta=60):
        self.len = self.__len__()
        self.past = []
        self.current = []
        self.future = []
        self.rest = []
        self.laterToday = []
        _dateTime = datetime.datetime(2015,1,1)

        if not isinstance(current_datetime, datetime.datetime):
            current_datetime = datetime.datetime.now()  # datetime.datetime
        currentTime = current_datetime.time()  # datetime.time
        currentDay = current_datetime.isoweekday() % 7  # integer

        for event in self:

# TODO: fix here
            # add attribute to event for diaplay
            event.days_texts = getScottyDaysText(event.times)
            event.building_texts = getScottyBuildingText(event.times)

# if today in days:
#   if both/some:
#     find a current time
#     if not happening:
#       find a later time
#   if just one:
#     find current time
#     if not happening;
#       use the rest
#   if none:
#     "on other days"

            inNearFutureTimeObj = None
            latestBeginTimeObj = None

            for timeObj in event.times:
                # Check if time and day exist
                if ((timeObj["days"] is not None) and (timeObj["begin"] is not None)
                    and (timeObj["end"] is not None)):

                    _beginTime = parseTime(timeObj["begin"])
                    _endTime = parseTime(timeObj["end"])

                    if currentDay in timeObj["days"]:  # this event is happening today
                        if _beginTime < currentTime < _endTime:  # and happening now
                            _diff = getTimeDifference(_beginTime, _endTime, current_datetime, "current")
                            _time = _dateTime + _diff
                            if _diff.seconds <= 3600:
                                event.diffText = "Ends in {} minutes".format(_time.minute)
                            else:
                                event.diffText = "Ends in {} h {} minutes".format(_time.hour, _time.minute)
                            self.current.append(event)
                            break
                        else:
                            # not happening now, temporarily store it
                            if latestBeginTimeObj is None or _beginTime > latestBeginTimeObj:
                                latestBeginTimeObj = timeObj
                            if (_beginTime > currentTime and
                                inMinutes(_beginTime) < inMinutes(currentTime) + time_delta):
                                inNearFutureTimeObj = timeObj
            # this event is not happening now, but still happening today
            if inNearFutureTimeObj is not None:  # in one hour!
                _beginTime = parseTime(timeObj["begin"])
                _endTime = parseTime(timeObj["end"])
                _diff = getTimeDifference(_beginTime, _endTime, current_datetime, "future")
                _time = _dateTime + _diff
                if _diff.seconds <= 3600:
                    event.diffText = "Begins in {} minutes".format(_time.minute)
                else:
                    event.diffText = "Begins in {} h {} minutes".format(_time.hour, _time.minute)
                self.future.append(event)
            elif latestBeginTimeObj is not None:  # ended or later today
                _latestBeginTime = parseTime(latestBeginTimeObj["begin"])
                _latestEndTime = parseTime(latestBeginTimeObj["end"])
                if _latestEndTime < currentTime:  # ended event
                    event.diffText = "{}:{}".format(_latestBeginTime.hour, _latestBeginTime.minute)
                    self.past.append(event)
                elif not (_latestBeginTime > currentTime and
                          inMinutes(_latestBeginTime) < inMinutes(currentTime) + time_delta):  # later today
                    event.diffText = "{}:{}".format(_latestBeginTime.hour, _latestBeginTime.minute)
                    self.laterToday.append(event)
            # happening on other days
            else:
                event.diffText = " ".join(event.days_texts)
                self.rest.append(event)


    def sortByTime(self, current_datetime=None):
        self.ready(current_datetime)
        return self.current + self.future + self.laterToday + self.past + self.rest


def getTimeDifference(begin_time, end_time, current_datetime, typ):
    # if not isinstance(currentDatetime, datetime.datetime):
    #     currentDatetime = datetime.datetime.now()
    currentDate = current_datetime.date()

    if typ == "current":
        diff = datetime.datetime.combine(currentDate, end_time) - current_datetime
        return diff
    elif typ == "future":
        diff = datetime.datetime.combine(currentDate, begin_time) - current_datetime
        return diff


def parseTime(time_string):
    return datetime.datetime.strptime(time_string, "%I:%M%p").time()
