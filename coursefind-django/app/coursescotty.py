# @file coursescotty.py
# @brief Contains the Event, Course etc. classes.
# @author Justin Chu (justinchuby@cmu.edu)


import datetime
import copy

try:
    from .utilities import *
    from . import cmu_prof
except:
    from utilities import *
    import cmu_prof


class Course(object):
    def __init__(self, scotty_dict):
        _PROPS = ["name", "department", "units", "semester", "desc",
                  "prereqs", "prereqs_obj", "coreqs", "coreqs_obj",
                  "lectures", "sections", "semester",
                  "courseid", "rundate", "semester_current"]
        self.scottyDict = copy.deepcopy(scotty_dict)
        for key in _PROPS:
            self.add(key, self.scottyDict.get(key))
        self.courseid = scotty_dict["id"]
        self.lectures = [Meeting(meeting) for meeting in self.scottyDict["lectures"]]
        self.sections = [Meeting(meeting) for meeting in self.scottyDict["sections"]]

    def __repr__(self):
        s = "</Course- {} />".format(self.__dict__)
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

        _KEYS = ["lectures", "sections"]

        for key in _KEYS:
            if self.__dict__[key] != []:
                for meeting in self.__dict__[key]:
                    output[key].append(LectureSection(self, meeting))
        return output

    def add(self, key, value):
        self.__dict__[key] = copy.deepcopy(value)

    def get(self, key):
        return copy.deepcopy(self.__dict__.get(key))


class Meeting(object):
    def __init__(self, meeting_dict):
        # _PROPS = ["instructors", "name", "times"]
        self.instructors = meeting_dict["instructors"]
        self.name = meeting_dict["name"]
        self.times = [TimeObj(time) for time in meeting_dict["times"]]

    def __repr__(self):
        s = "</Meeting- {} />".format(self.__dict__)
        return s

    def get(self, key):
        return copy.deepcopy(self.__dict__.get(key))

    def expose(self):
        return copy.deepcopy(self.__dict__)


class TimeObj(object):
    def __init__(self, time_dict):
        _PROPS = ["begin", "end", "days", "location", "building", "room"]
        for key in _PROPS:
            self.__dict__[key] = time_dict[key]
        self.begin = parseTime(self.begin)
        self.end = parseTime(self.end)

    def __repr__(self):
        s = "</TimeObj- {} />".format(self.__dict__)
        return s

    def get(self, key):
        return copy.deepcopy(self.__dict__.get(key))


class LectureSection(object):
    def __init__(self, course_obj, meeting_obj, typ=""):
        _KEYS = ["name",  "units", "semester", "desc", "coreqs", "prereqs",
                "courseid", "rundate", "department", "semester_current"]
        # _PROPS = ["courseid", "name", "units", "lecsec", "times", "instructors",
        #               "rundate", "department", "coreqs", "prereqs", "type"]
        self.type = typ
        self.lecsec = meeting_obj.get("name")
        _meetingDict = meeting_obj.expose()
        for key in _KEYS:
            self.add(key, course_obj.get(key))
        for key in _meetingDict:
            if key != "name":
                self.add(key, meeting_obj.get(key))

        # add days_text and building_text for the web app
        for timeObj in self.times:
            if timeObj.building is None:
                self.building = "TBA"
            if timeObj.room is None:
                self.room = "TBA"
            timeObj.days_text = getDaysText(timeObj.days)
            timeObj.building_text = getBuildingText(timeObj.building)
# TODO: Delete after the API supports full names
        # Get full names of instructors
        self.instructors = cmu_prof.getFullNames(self.instructors,
                                                 self.courseid[:2]+
                                                 self.courseid[3:])

    def __repr__(self):
        s = "</LectureSection- {} />".format(self.__dict__)
        return s

    def add(self, key, value):
        self.__dict__[key] = copy.deepcopy(value)

    def expose(self):
        return copy.deepcopy(self.__dict__)


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
    def ready(self, current_datetime=None, time_delta=60, current_day=None):
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
        if not isinstance(current_day, int):
            currentDay = current_datetime.isoweekday() % 7  # integer
        else:
            currentDay = current_day % 7

        for event in self:
            event.days_texts = getDaysTextsFromTimes(event.times)

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

            isHappening = False
            inNearFutureTimeObj = None
            latestBeginTimeObj = None

            for timeObj in event.times:
                # Check if time and day exist
                if ((timeObj.days is not None) and (timeObj.begin is not None)
                    and (timeObj.end is not None)):

                    # Add beginTime and endTime for compatibility
                    timeObj.beginTime = timeObj.begin
                    timeObj.endTime = timeObj.end

                    _beginTime = timeObj.begin
                    _endTime = timeObj.end

                    # this event is happening today
                    if currentDay in timeObj.days:
                        # and happening now
                        if _beginTime <= currentTime <= _endTime:
                            event.matchedTime = timeObj
                            _diff = getTimeDifference(_beginTime, _endTime, current_datetime, "current")
                            _time = _dateTime + _diff
                            if _diff.seconds <= 3600:
                                event.diffText = "Ends in {} minutes".format(_time.minute)
                            else:
                                event.diffText = "Ends in {} h {} minutes".format(_time.hour, _time.minute)

                            self.current.append(event)
                            isHappening = True
                            break
                        # not happening now, temporarily store it
                        else:
                            if latestBeginTimeObj is None or _beginTime > latestBeginTimeObj.begin:
                                latestBeginTimeObj = timeObj
                            if (_beginTime > currentTime and
                                inMinutes(_beginTime) < inMinutes(currentTime) + time_delta):
                                inNearFutureTimeObj = timeObj

            # this event is not happening now, but still happening today
            # in one hour!
            if not isHappening:
# DEGUG
                # print("%s %s is not happening" % (event.name, event.lecsec))
                if inNearFutureTimeObj is not None:
                    event.matchedTime = inNearFutureTimeObj
                    _beginTime = inNearFutureTimeObj.begin
                    _endTime = inNearFutureTimeObj.end

                    _diff = getTimeDifference(_beginTime, _endTime, current_datetime, "future")
                    _time = _dateTime + _diff
                    if _diff.seconds <= 3600:
                        event.diffText = "Begins in {} minutes".format(_time.minute)
                    else:
                        event.diffText = "Begins in {} h {} minutes".format(_time.hour, _time.minute)
                    self.future.append(event)

                # ended or later today
                elif latestBeginTimeObj is not None:
                    event.matchedTime = latestBeginTimeObj
                    _latestBeginTime = latestBeginTimeObj.begin
                    _latestEndTime = latestBeginTimeObj.end

                    # ended event
                    if _latestEndTime < currentTime:
                        event.diffText = _latestBeginTime.strftime("%-H:%M")
                        self.past.append(event)

                    # later today
                    elif not (_latestBeginTime > currentTime and
                              inMinutes(_latestBeginTime) < inMinutes(currentTime) + time_delta):
                        event.diffText = _latestBeginTime.strftime("%-H:%M")
                        self.laterToday.append(event)

                # happening on other days
                else:
# TODO: the line below is a patch
                    event.matchedTime = event.times[0]
                    event.diffText = " ".join(event.days_texts)
                    self.rest.append(event)

    def sortByTime(self, current_datetime=None):
        self.ready(current_datetime)
        return self.current + self.future + self.laterToday + self.past + self.rest


def getCurrentSemester(course_dict=None):
    try:
        return course_dict["lectures"][0].semester_current
    except:
        pass
    try:
        return course_dict["sections"][0].semester_current
    except:
        def getSemester(year, month):
            if 1 <= month <= 4:
                semester = "Spring"
            elif 5 <= month <= 6:
                semester = "Summer-1"
            elif month == 7:
                semester = "Summer-2"
            else:
                semester = "Fall"
            return "%s %s" % (semester, str(year))
        currentYear = datetime.date.today().year
        currentMonth = datetime.date.today().month
        return getSemester(currentYear, currentMonth)


def getCatalogDate(course_dict):
    try:
        return course_dict["lectures"][0].rundate
    except:
        pass
    try:
        return course_dict["sections"][0].rundate
    except:
        pass
    return ""
