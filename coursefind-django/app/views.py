from django.shortcuts import render

import datetime
import re
import random

try:
    from . import catalogsearcher, coursecat
except:
    import catalogsearcher, coursecat


# def loading(request):
#     return render(request, 'app/loading.html')


def getText(displayMode, tab, eventList):
    result = None
    try:
        if "search" in displayMode:
            if "room" not in displayMode:
                if tab == "lecture" or tab == "section":
                    if len(eventList) > 98:
                        result = "Found more than 98 {}s.".format(tab)
                    elif len(eventList) > 1:
                        result = "Found {} {}s.".format(len(eventList), tab)
                    elif len(eventList) == 1:
                        result = "Found one {}.".format(tab)
                    elif len(eventList) == 0:
                        result = "Found no {} that matches.".format(tab)

                    if "looseSearched" in displayMode:
                        result += "\nBut no {}'s name satisfies the whole search text.".format(tab)

        elif "time" in displayMode:
            displayTime = displayMode["time"].strftime("%H:%M")
            if tab == "lecture" or tab == "section":
                if len(eventList.current) > 98:
                    result = "There are more than 98 {}s at {}.".format(tab, displayTime)
                elif len(eventList.current) > 1:
                    result = "There are {} {}s at {}.".format(len(eventList.current), tab, displayTime)
                elif len(eventList.current) == 1:
                    result = "One {} happening at {}.".format(tab, displayTime)
                elif len(eventList.future) > 0:
                    result = "There are {}s in an hour after {}.".format(tab, displayTime)
                elif len(eventList) == 0:
                    result = "No {} happening at {}. Take a break :)".format(tab, displayTime)

        elif "current" in displayMode:
            if tab == "lecture" or tab == "section":
                if len(eventList.current) > 98:
                    result = "There are currently more than 98 {}s happening.".format(tab)
                elif len(eventList.current) > 1:
                    result = "There are currently {} {}s happening.".format(len(eventList.current), tab)
                elif len(eventList.current) == 1:
                    result = "One {} happening at this time.".format(tab)
                elif len(eventList.future) > 0:
                    result = "There are {}s happening in an hour.".format(tab)
                elif len(eventList) == 0:
                    result = "No {} happening at this time. Take a break :)".format(tab)

    except:
        pass
    return result


def home(request, **kwargs):
# DEBUG
    print(request.GET, request.POST)
    currentDatetime = datetime.datetime.now()
    searchDatetime = currentDatetime
    currentDate = currentDatetime.date()
    searchDate = currentDate
    currentTime = currentDatetime.time()
    searchTime = currentTime
    # currentDay = currentDatetime.weekday()
    # timeInMinutes = coursecat.inMinutes(currentTime)
    courses = []
    searchText = ""
    shouldSearch = True
    looseSearched = False
    displayMode = {"current": None}
    courses_lec = coursecat.CourseList()
    courses_sec = coursecat.CourseList()
    lecture_tab_text = ""
    section_tab_text = ""

    mainpage_toast = None
    SEARCH_TIPS = ("a course number",
                   "name of an instructor",
                   "name of a course",
                   "a room number",
                   "a building",
                   "a time")
    search_tip = None

    if request.method == "GET":
        data = dict(request.GET)
        # searchDate = ""

        # set currentDatetime as the search time
        # if "date" in data:
        #     if isinstance(data["date"], list):
        #         searchDate = data["date"][0]
        #     elif isinstance(data["date"], str):
        #         searchDate = data["date"]
        #     match = re.search("(\d\d?)\s*([a-zA-Z]*),\s(\d\d\d\d)", searchDate)
        #     if match:
        #         currentDate = datetime.datetime.strptime(match.group(), "%d %b, %Y").date()
        #         currentDatetime = datetime.datetime.combine(currentDate, currentTime)
        #     elif searchDate != "":
        #         searchDate = currentDate.strftime("%d %b, %Y")
        if "q" in data:
            # searching
            displayMode["search"] = None

            if isinstance(data["q"], list):
                searchText = data["q"][0]
            elif isinstance(data["q"], str):
                searchText = data["q"]
            searchTextWithoutTime = searchText
            # find time first
            match = re.search("\d\d?:\d\d", searchText)
            if match:
                try:
                    # the 2015 1 1 has no meaning, just to construct a datetime instance
                    searchTime = datetime.datetime.strptime("2015 1 1 %s" % match.group(), "%Y %m %d %H:%M").time()
                    searchDatetime = datetime.datetime.combine(searchDate, searchTime)
                    displayMode["time"] = searchTime
# DEBUG
                    # print(searchDatetime)
                except:
                    print("fail to parse time")
                # delete time from search text
                searchTextWithoutTime = re.sub("\d\d?:\d\d", " ", searchText)

            if coursecat.getSearchable(searchTextWithoutTime) == []:
# TODO needs to change the displayMode according to search date
                del displayMode["search"]
                courses = catalogsearcher.getCurrentCourses(currentDatetime=searchDatetime)
            else:
                shouldSearch, mainpage_toast = catalogsearcher.presearch(searchTextWithoutTime)
                if shouldSearch:
                    courses = catalogsearcher.search(searchTextWithoutTime)

                    if courses == []:
                        # if no course returns
                        courses = catalogsearcher.search(searchTextWithoutTime, looseField={"name"})
                        if courses != []:
                            # now there are courses!
                            looseSearched = True
                            displayMode["looseSearched"] = None
        else:
            courses = catalogsearcher.getCurrentCourses(currentDatetime=searchDatetime)

    # put courses into lectures and sections
    if courses != []:
        for course in courses:
            if "lec" in course.typ:
                courses_lec.append(course)
            elif "sec" in course.typ:
                courses_sec.append(course)

        # for course in courses_lec:
        #     if course.number == "15112" and "search" in displayMode:
        #         mainpage_toast = "I love 112 !"

        # dont forget to call ready
        courses_lec.ready(currentDatetime=searchDatetime)
        courses_sec.ready(currentDatetime=searchDatetime)

    # generate the result prompt
    lecture_tab_text = getText(displayMode, "lecture", courses_lec)
    section_tab_text = getText(displayMode, "section", courses_sec)
    if len(courses_lec) == 0 and len(courses_sec) > 0:
        lecture_tab_text += " But sections are found."

    # get different time divisions
    time_flags = [["current", "Now happening"],
                 ["future", "In an hour"],
                 ["laterToday", "Later today"],
                 ["past", "Ended"],
                 ["rest", "On other days"]]

    search_tip = "Try searching for " + random.choice(SEARCH_TIPS)

# DEBUG
    # print("searching:", searchText)

    context = {'searchText': searchText,
               'courses_lec': courses_lec,
               'courses_sec': courses_sec,
               'lecture_tab_text': lecture_tab_text,
               'section_tab_text': section_tab_text,
               'mainpage_toast': mainpage_toast,
               'displayMode': displayMode,
               'time_flags': time_flags,
               'search_tip': search_tip}

    return render(request, 'app/index.html', context)


def about(request):
    context = dict()
    return render(request, 'app/about.html', context)

def disclaimer(request):
    context = dict()
    return render(request, 'app/disclaimer.html', context)
