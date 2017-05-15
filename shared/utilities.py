import re
import datetime
import string
import copy
try:
    import cmu_info
except:
    from . import cmu_info


def formatErrMsg(e, header=""):
    if not header.endswith("_"):
        header += "_"
    errmsg = "{}ERROR-{} STR-<{}> REPR-<{}>".format(header, datetime.datetime.now().isoformat(), str(e), repr(e))
    return errmsg


SOC_TABLE_ORDER = {
    "number": 0,
    "name": 1,
    "units": 2,
    "lecsec": 3,
    "days": 4,
    "beginTime": 5,
    "endTime": 6,
    "room": 7,
    "location": 8,
    "instructor": 9
}


##
## @brief      Empty object
##
class Empty(object):
    def __init__(self, s=" "):
        self.string = s

    def __eq__(self, other):
        return isinstance(other, Empty) or str(self) == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__class__.__name__ + "()"

    def __str__(self):
        return self.string

    def __iter__(self):
        return iter(str(self))

    def isdigit(self):
        return False


##
## @brief      A dictionary whose values are lists, with a concat() method that
##             concatenates two Listdict object's values.
##
class Listdict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def concat(self, other):
        _other = copy.deepcopy(other)
        for key, value in _other.items():
            if key in self:
                self[key] += value
            else:
                self[key] = value

##
## @brief      Represent a time in minutes.
##
## @param      time  Can be (datetime.time), (datetime.datetime) or (datetime.timedelta).
##
## @return     (int) minutes, or and Empty object if failed to convert.
##
def inMinutes(time):
    # represent a time in minutes
    if isinstance(time, datetime.time) or isinstance(time, datetime.datetime):
        return time.hour * 60 + time.minute
    elif isinstance(time, datetime.timedelta):
        return time.seconds // 60
    else:
        return Empty()


##
## @brief      Eliminates spaces and makes each word in lower case.
##
## @param      s          The input string.
## @param      separator  The separator in the string
##
## @return     A list of strings.
##
def splitString(s, separator=","):
    return [elem.strip().lower() for elem
            in s.split(separator) if elem.strip() != ""]


##
## @brief      Gets the string rid of punctuations.
##
## @param      s     (str)
##
## @return     (str)
##
def eliminatePunc(s):
    return re.sub(r"[%s]" % string.punctuation, " ", s)


def getSearchable(s):
    return splitString(eliminatePunc(s).lower(), " ")


def getDaysText(days):
    try:
        result = convertDaysToTexts(days)
        return ", ".join(result)
    except:
        return "TBA"


def getDaysTextsFromTimes(times):
    return convertDaysToTexts(getDaysFromTimes(times))


def getDaysFromTimes(times):
    days = set()
    for time in times:
        try:
            for day in time.get("days"):
                if type(day) == int:
                    days.add(day % 7)
        except:
            pass
    return sorted(days)


##
## @brief      Convert days to their text representation in a list.
##
## @param      days  (int)(list) The days
##
## @return     A list of strings.
##
def convertDaysToTexts(days):
    _DAYS = {1: "Mon",
             2: "Tue",
             3: "Wed",
             4: "Thu",
             5: "Fri",
             6: "Sat",
             0: "Sun"}
    result = []
    try:
        for day in days:
            if day in _DAYS:
                result.append(_DAYS[day])
    except:
        pass
    return result


##
## @brief      Gets the full name of a building from its abbreviation.
##
## @param      building  (str)
##
## @return     (str)
##
def getBuildingText(building):
    _CMU_BUILDINGS_FROM_ABBR = cmu_info.CMU_BUILDINGS_FROM_ABBR
    if building is None:
        return "TBA"
    elif building in _CMU_BUILDINGS_FROM_ABBR:
        return _CMU_BUILDINGS_FROM_ABBR[building]
    else:
        return building

##
## @brief      Gets the name of the department that offers the course.
##
## @param      number_searchable
##
## @return     The name of the department if found, original input of not found.
##
def getCourseDepartment(number_searchable):
    try:
        num = number_searchable[0]
    except:
        return ""

    _CMU_NUMBER_DEPARTMENTS = cmu_info.CMU_NUMBER_DEPARTMENTS

    if num in _CMU_NUMBER_DEPARTMENTS:
        return _CMU_NUMBER_DEPARTMENTS[num]
    else:
        return num


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
    try:
        return datetime.datetime.strptime(time_string, "%I:%M%p").time()
    except:
        pass
    try: 
        return datetime.datetime.strptime(time_string, "%H:%M").time()
    except:
        return None


##
## @brief      Get the mini term.
##
## @return     (int) The current mini if no date is provided.
##
def getMini(current_date=None):
    if current_date is None:
        current_date = datetime.date.today()
    elif isinstance(current_date, datetime.datetime):
        current_date = current_date.date()
    year = current_date.year
    if datetime.date(year, 8, 20) < current_date <= datetime.date(year, 10, 15):
        return 1
    elif datetime.date(year, 10, 15) < current_date <= datetime.date(year, 12, 31):
        return 2
    elif datetime.date(year, 1, 1) <= current_date <= datetime.date(year, 3, 15):
        return 3
    elif datetime.date(year, 3, 15) < current_date <= datetime.date(year, 5, 15):
        return 4
    elif datetime.date(year, 5, 15) < current_date <= datetime.date(year, 6, 25):
        return 5
    elif datetime.date(year, 6, 25) < current_date <= datetime.date(year, 8, 20):
        return 6
    return 0


def getCurrentIndex():
    return getIndexFromDate(datetime.date.today())


def getIndexFromDate(date):
    mini = getMini(date)
    if 1 <= mini <= 2:
        semester = "f"
    elif 3 <= mini <= 4:
        semester = "s"
    elif mini == 5:
        semester = "m1"
    else:
        semester = "m2"
    index = semester + str(date.year)[2:]
    return index


class _Tests():
    @staticmethod
    def test_parseTime():
        assert(datetime.time(8, 15) == parseTime("8:15am"))
        assert(datetime.time(20, 15) == parseTime("8:15PM"))
        assert(datetime.time(8, 0) == parseTime("8:00"))
        assert(datetime.time(20, 0) == parseTime("20:00"))
