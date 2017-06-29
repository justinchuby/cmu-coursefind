# @file cmu_course.py
# @brief The module for Course and Meeting object.
# @author Justin Chu (justinchuby@cmu.edu)


import copy
from shared import utils


class Course(object):
    _PROPS = ("name", "department", "units", "desc",
              "prereqs", "prereqs_obj", "coreqs", "coreqs_obj",
              "lectures", "sections", "courseid", "rundate", "semester")

    def __init__(self, scotty_dict):
        self.scottyDict = copy.deepcopy(scotty_dict)
        for key in self._PROPS:
            self.__dict__[key] = self.scottyDict.get(key)
        self.courseid = scotty_dict["id"]
        self.lectures = [Meeting(self, meeting) for meeting in self.scottyDict["lectures"]]
        self.sections = [Meeting(self, meeting) for meeting in self.scottyDict["sections"]]
        # Using a list for self.instructors to keep the order
        self.instructors = []
        for lec in self.lectures:
            for instructor in lec.instructors:
                if instructor not in self.instructors:
                    self.instructors.append(instructor)

    def __repr__(self):
        s = "</Course- {} />".format(self.__dict__)
        return s

    def get(self, key):
        return copy.deepcopy(self.__dict__.get(key))

    def dict(self):
        # TODO: export dict from data in the object
        return copy.deepcopy(self.scottyDict)


class Meeting(object):
    # _PROPS = ["name", "instructors", "times"]
    def __init__(self, course, meeting_dict):
        self.course = course
        self.name = meeting_dict["name"]
        self.instructors = meeting_dict["instructors"]
        self.times = [TimeObj(time) for time in meeting_dict["times"]]

    def __repr__(self):
        s = "</Meeting- {} />".format(self.__dict__)
        return s

    def get(self, key):
        return copy.deepcopy(self.__dict__.get(key))

    def isHappeningAt(self, date_time):
        for timeObj in self.times:
            if timeObj.isHappeningAt(date_time):
                return True
        return False

    def isHappeningOn(self, day):
        for timeObj in self.times:
            if timeObj.isHappeningOn(day):
                return True
        return False


class TimeObj(object):
    _PROPS = ("begin", "end", "days", "location", "building", "room")

    def __init__(self, time_dict):
        for key in self._PROPS:
            self.__dict__[key] = time_dict[key]
        self.begin = utils.parse_time(self.begin)
        self.end = utils.parse_time(self.end)

    def __repr__(self):
        s = "</TimeObj- {} />".format(self.__dict__)
        return s

    def get(self, key):
        return copy.deepcopy(self.__dict__.get(key))

    def isHappeningAt(self, date_time):
        time = date_time.time()
        day = date_time.isoweekday() % 7  # integer
        if self.isHappeningOn(day) and (self.begin <= time < self.end):
            return True
        return False

    def isHappeningOn(self, day):
        return (day in self.days)
