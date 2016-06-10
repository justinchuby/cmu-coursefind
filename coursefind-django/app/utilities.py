import re
import datetime
import string
try:
    import cmu_info
except:
    from . import cmu_info

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


# def parseTime(s, frm=None):
#     h = m = 0
#     if frm is None:
#         if ("AM" in s.upper()) or ("PM" in s.upper()):
#             return parseTime(s, "SOC")
#         else:
#             return parseTime(s, "CTG")

#     elif frm == "CTG":
#         try:
#             # time represented in minutes
#             t = int(s)
#             h = t // 60
#             m = t % 60
#             return datetime.time(h, m)
#         except:
#             return None

#     elif frm == "SOC":
#         # mark does not support 24 hour format
#         # may also use datetime.strptime(date_string, format)
#         try:
#             match = re.search("(\d*):(\d\d)([AP]M)", s)
#             if match:
#                 h = int(match.group(1)) % 12
#                 if match.group(3) == "PM":
#                     h += 12
#                 m = int(match.group(2))
#                 return datetime.time(h, m)
#             else:
#                 return None
#         except:
#             return None

#     return None


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
    _DAYS = {"1": "Mon",
             "2": "Tue",
             "3": "Wed",
             "4": "Thu",
             "5": "Fri",
             "6": "Sat",
             "0": "Sun"}
    result = []
    for day in days:
        if day in _DAYS:
            result.append(_DAYS[day])
    return ", ".join(result)


def getScottyDaysText(times):
    _DAYS = {1: "Mon",
             2: "Tue",
             3: "Wed",
             4: "Thu",
             5: "Fri",
             6: "Sat",
             0: "Sun"}
    days_texts = []
    for time in times:
        _days = []
        if time["days"] is not None:
            for day in time["days"]:
                if day in _DAYS:
                    _days.append(_DAYS[day])
        days_texts.append(", ".join(_days))

    return days_texts


##
## @brief      Gets the full name of a building from its abbreviation.
##
## @param      building  (str)
##
## @return     (str)
##
def getBuildingText(building):
    _CMU_BUILDINGS_FROM_ABBR = cmu_info.CMU_BUILDINGS_FROM_ABBR
    if building in _CMU_BUILDINGS_FROM_ABBR:
        return _CMU_BUILDINGS_FROM_ABBR[building]
    else:
        return building


def getScottyBuildingText(times):
    _CMU_BUILDINGS_FROM_ABBR = cmu_info.CMU_BUILDINGS_FROM_ABBR
    buildings = []
    for time in times:
        building = time["building"]
        if building is not None:
            if building in _CMU_BUILDINGS_FROM_ABBR:
                buildings.append(_CMU_BUILDINGS_FROM_ABBR[building])
            else:
                buildings.append(building)
        else:
            buildings.append("")
    return buildings


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

# def DaysToBinary(s):
#     # convert days into binary representation "MTWRFSU"
#     try:
#         _daysString = "MTWRFSU"
#         if (isinstance(self.days, str) and
#             self.days != "TBA" and self.days[0] in _daysString):
#             days = 0
#             for i in len(_daysString):

#                 if _daysString[i] in self.days:

#     except:
#         print("failed to convert days")
#         self.days = -1


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