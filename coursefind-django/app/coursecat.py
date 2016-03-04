import re
import datetime
import string
try:
    from utilities import *
except:
    from .utilities import *


class EventList(list):
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


    def ready(self, currentDatetime=None, timeDelta=60):
        self.len = self.__len__()
        self.past = []
        self.current = []
        self.future = []
        self.rest = []
        self.laterToday = []
        _dateTime = datetime.datetime(2015,1,1)
        # timeDelta = datetime.timedelta(minutes = timeDelta)
        if not isinstance(currentDatetime, datetime.datetime):
            currentDatetime = datetime.datetime.now()
        currentTime = currentDatetime.time()
        currentDay = str(currentDatetime.weekday())

        for event in self:

            # add attribute to event for diaplay
            event.days_text = getDaysText(event.days)
            event.building_text = getBuildingText(event.building)
            event.department = getCourseDepartment(event.number_searchable)

            # try:
            if currentDay in event.days_searchable:
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
            # except:
                # pass

    # def filter(self, currentDatetime, mode, timeDelta=60):
    #     timeDelta = datetime.timedelta(minutes = time)
    #     currentTime = currentDatetime.time()
    #     currentDay = currentDatetime.weekday()
    #     result = []
    #     for event in self:
    #         isInSpan = False
    #         try:
    #             if mode == "current":
    #                 isInSpan = event.intBeginTime < currentTime < event.intEndTime
    #             elif mode == "future":
    #                 isInSpan = (event.intBeginTime > currentTime and
    #                         event.intBeginTime < currentTime + timeDelta)
    #             elif mode == "past":
    #                 isInSpan = (event.intEndTime < currentTime)
    #             if (isInSpan and currentDay in event.days_searchable):
    #                 result.append(event)
    #         except:
    #             pass
    #     return result

    # def current(self, currentDatetime=None):
    #     # return filter(self, currentDatetime, "current")
    #     return self.current

    # def future(self, currentDatetime=None, timeDelta=60):
    #     # return filter(self, currentDatetime, "future", timeDelta)
    #     return self.future

    # def past(self, currentDatetime=None):
    #     # return filter(self, currentDatetime, "past")
    #     return self.past


    def sortByTime(self, currentDatetime=None):
        self.ready(currentDatetime)
        return self.current + self.future + self.laterToday + self.past + self.rest
        



class CourseList(EventList):
    pass


class Event(object):
    EMPTY = Empty()
    COMMA = ";"
    KEYS = ["number", "name", "units", "lecsec", "days",
            "beginTime", "endTime", "building", "room", "city", "instructor",
            "typ", "beginDate", "endDate", "location", "objectId"]
    SEARCHABLE_KEYS = ["number_searchable", "name_searchable",
                       "days_searchable", "intBeginTime", "intEndTime",
                       "city_searchable", "instructor_searchable",
                       ]

    def __init__(self, data=None):
        self.number = Event.EMPTY
        self.name = Event.EMPTY
        self.units = Event.EMPTY
        self.lecsec = Event.EMPTY
        self.days = Event.EMPTY
        self.beginTime = Event.EMPTY
        self.endTime = Event.EMPTY
        self.building = Event.EMPTY
        self.room = Event.EMPTY
        self.city = Event.EMPTY
        self.instructor = Event.EMPTY
        self.typ = Event.EMPTY
        self.beginDate = Event.EMPTY
        self.endDate = Event.EMPTY
        self.location = Event.EMPTY
        self.objectId = Event.EMPTY
        for key in Event.SEARCHABLE_KEYS:
            self.__dict__[key] = Event.EMPTY

    def __repr__(self):
        L = self.getListRepr()
        return "coursecat." + self.__class__.__name__ + "(" + repr(L) + ")"

    def __str__(self):
        L = self.getListRepr()
        L = [str(elem).replace(",", Event.COMMA) for elem in L]
        return ",".join(L)

    def __eq__(self, other):
        if isinstance(other, Event):
            if self.objectId != Event.EMPTY and other.objectId != Event.EMPTY:
                return self.objectId == other.objectId
            else:
                for key in Event.KEYS:
                    if self.get(key) != other.get(key):
                        return False
                return True
        return False

    def __ne__(self, other):
        return self.__eq__(other)

    def isCompleted(self):
        pass

    def isEmpty(self):
        d = self.__dict__
        for key in SOC_TABLE_ORDER:
            if key in d:
                value = d[key]
                if value != Event.EMPTY and value is not None:
                    return False

    def isLegal(self):
        pass

    def content(self):
        # returns a dictionary
        return self.__dict__

    def refresh(self, _key=None):
        # for key, value in self.__dict__.items():
        #     if isinstance(value, str):
        #         self.__dict__[key] = value.replace(",", Event.COMMA)
        if _key is None or _key == "beginTime":
            if isinstance(self.beginTime, str) and self.beginTime != Event.EMPTY:
                self.beginTime = parseTime(self.beginTime, "CTG")
        if _key is None or _key == "beginTime":
            if isinstance(self.endTime, str) and self.endTime != Event.EMPTY:
                self.endTime = parseTime(self.endTime, "CTG")

    def updateKey(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value
        self.refresh(key)

    def getType(self):
        return Event.EMPTY

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def getDictRepr(self):
        keys = Event.KEYS
        values = [self.number, self.name, self.units, self.lecsec, self.days,
                  self.beginTime, self.endTime, self.building, self.room,
                  self.city, self.instructor, self.typ, self.beginDate,
                  self.endDate, self.location, self.objectId]
        d = dict(zip(keys, values))
        # d["beginTime"] = inMinutes(d["beginTime"])
        # d["endTime"] = inMinutes(d["endTime"])
        return d

    def getListRepr(self):
        keys = Event.KEYS
        d = self.getDictRepr()
        L = [d[key] for key in keys]
        return L

    def JSONDict(self):
        d = self.getDictRepr()
        d["beginTime"] = inMinutes(d["beginTime"])
        d["endTime"] = inMinutes(d["endTime"])
        for key, value in d.items():
            d[key] = str(value)
        try:
            d["intBeginTime"] = int(d["beginTime"])
        except:
            pass
        try:
            d["intEndTime"] = int(d["endTime"])
        except:
            pass

        d["name_searchable"] = getSearchable(d["name"])
        if type(d["days"]) == str:
            d["days_searchable"] = [day for day in d["days"]]
        if type(d["instructor"]) == str:
            d["instructor_searchable"] = getSearchable(d["instructor"])
        if type(d["city"]) == str:
            d["city_searchable"] = splitString(d["city"], ",")
        try:
            if type(d["number"]) == str:
                d["number_searchable"] = [d["number"][:2], d["number"][2:]]
        except:
            pass
        if len(d["objectId"]) != 10:
            del d["objectId"]
        return d


class Course(Event):
    def __init__(self, data=None):
        super().__init__()
        if type(data) == dict:
            for key in Event.KEYS:
                if key in data:
                    self.updateKey(key, data[key])
            for key in Event.SEARCHABLE_KEYS:
                if key in data:
                    self.updateKey(key, data[key])

            # self.number = data.get("number", Course.EMPTY)
            # self.name = data.get("name", Course.EMPTY)
            # self.units = data.get("units", Course.EMPTY)
            # self.lecsec = data.get("lecsec", Course.EMPTY)
            # self.days = data.get("days", Course.EMPTY)
            # self.beginTime = data.get("beginTime", Course.EMPTY)
            # self.endTime = data.get("endTime", Course.EMPTY)
            # self.building = data.get("building", Course.EMPTY)
            # self.room = data.get("room", Course.EMPTY)
            # self.city = data.get("city", Course.EMPTY)
            # self.instructor = data.get("instructor", Course.EMPTY)
            # self.typ = data.get("typ", Course.EMPTY)
            # self.beginDate = data.get("beginDate", Course.EMPTY)
            # self.endDate = data.get("endDate", Course.EMPTY)
            # self.location = data.get("location", Course.EMPTY)
            # self.objectId = data.get("objectId", Course.EMPTY)
        self.refresh()

    def isLegal(self):
        d = self.__dict__
        courseNumber = d.get("number", Event.EMPTY)
        if (not courseNumber == Event.EMPTY) and (not courseNumber.isdigit()):
            # course number cant be a list
            return False
        if self.name == "TBA":
            return False
        if self.room == "DNM" or self.building == "DNM":
            return False
        if self.beginTime == Event.EMPTY:
            return False
        return True

    def getType(self):
        if isinstance(self.lecsec, str):
            if "Lec" in self.lecsec:
                # A lecture
                return ["lec"]
            else:
                match = re.search("(\d)(\d)", self.lecsec)
                if match:
                    # mini lecture
                    return ["lec", "m"+match.group(2)]
                match = re.search("([a-zA-Z])(\d)", self.lecsec)
                if match:
                    # mini section
                    return ["sec", "m"+match.group(2)]
                match = re.search("[a-zA-Z]*", self.lecsec)
                if match:
                    # section
                    return ["sec"]
        return Event.EMPTY


class SOCCourse(Course):
    def __init__(self, data=None):
        super().__init__()
        # data should be a list
        if isinstance(data, list) and (len(data) >= 10):
            self.number = data[0]
            self.name = data[1]
            self.units = data[2]
            self.lecsec = data[3]
            self.days = data[4]
            self.beginTime = data[5]
            self.endTime = data[6]
            _room = data[7].strip().split(" ")
            if len(_room) == 1:
                self.room = data[7]
            elif len(_room) > 1:
                self.building = _room[0]
                self.room = " ".join(_room[1:])

            self.city = data[8]
            self.instructor = data[9]
        self.refresh()

    def refresh(self, _key=None):
        # super().refresh deleted

        # get rid of commas
        # for key, value in self.__dict__.items():
        #     if isinstance(value, str):
        #         self.__dict__[key] = value.replace(",", Event.COMMA)

        # convert time into datetime type
        if _key is None or _key == "beginTime":
            if isinstance(self.beginTime, str) and self.beginTime != Event.EMPTY:
                self.beginTime = parseTime(self.beginTime, "SOC")
        if _key is None or _key == "endTime":
            if isinstance(self.endTime, str) and self.endTime != Event.EMPTY:
                self.endTime = parseTime(self.endTime, "SOC")

        # convert day of the week into 0-6 representation
        if _key is None or _key == "days":
            try:
                if type(self.days) == str and self.days != "TBA":
                    days = self.days
                    for s, n in zip("MTWRFSU", "0123456"):
                        days = days.replace(s, n)
                    self.days = days
                else:
                    self.days = " "
            except:
                # print("failed to convert days")
                pass

        if _key is None or _key == "room":
            if "TBA" in self.room:
                self.building = "TBA"

        # # split the building and room number
        # if _key is None or _key == "room":

        # get the type attribute
        self.typ = self.getType()

    def isCompleted(self):
        L = [self.number, self.name, self.units, self.lecsec, self.days,
             self.beginTime, self.endTime, self.room, self.city, self.instructor]
        return not((None in L) or (Event.EMPTY in L))


#################################

# def test_Course():
#     print("testing testCourses...")
#     L1 = ["12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345"]
#     course1 = SOCCourse(L1)
#     assert(course1.isLegal() is True)
#     L2 = [" ", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345"]
#     course2 = SOCCourse(L2)
#     assert(course2.isLegal() is True)
#     assert(course2.isEmpty() is False)
#     L3 = ["Archi", "12345", "12345", " ", "12345", "12345", "12345", "12345", "12345", "12345"]
#     course3 = SOCCourse(L3)
#     assert(course3.isLegal() is False)
#     assert(course3.isEmpty() is False)
#     print("Passed!")


def testAll():
    # test_Course()

# if __name__ == '__main__':
#     testAll()
