from django.shortcuts import render

import datetime
import re
import random

try:
    from . import catalogsearcher_es, coursescotty
except:
    import catalogsearcher_es, coursescotty


def getText(display_mode, tab, event_list):
    result = None
    try:
        if "search" in display_mode:
            if "room" not in display_mode:
                if tab == "lecture" or tab == "section":
                    if len(event_list) > 1:
                        result = "Found {} {}s.".format(len(event_list), tab)
                    elif len(event_list) == 1:
                        result = "Found one {}.".format(tab)
                    elif len(event_list) == 0:
                        result = "Found no {} that matches.".format(tab)

                    if "looseSearched" in display_mode:
                        result += "\nBut no {}'s name satisfies the whole search text.".format(tab)

        elif "time" in display_mode:
            displayTime = display_mode["time"].strftime("%H:%M")
            if tab == "lecture" or tab == "section":
                if len(event_list.current) > 1:
                    result = "There are {} {}s at {}.".format(len(event_list.current), tab, displayTime)
                elif len(event_list.current) == 1:
                    result = "One {} happening at {}.".format(tab, displayTime)
                elif len(event_list.future) > 0:
                    result = "There are {}s in an hour after {}.".format(tab, displayTime)
                elif len(event_list) == 0:
                    result = "No {} happening at {}. Take a break :)".format(tab, displayTime)

        elif "current" in display_mode:
            if tab == "lecture" or tab == "section":
                if len(event_list.current) > 1:
                    result = "There are currently {} {}s happening.".format(len(event_list.current), tab)
                elif len(event_list.current) == 1:
                    result = "One {} happening at this time.".format(tab)
                elif len(event_list.future) > 0:
                    result = "There are {}s happening in an hour.".format(tab)
                elif len(event_list) == 0:
                    result = "No {} happening at this time. Take a break :)".format(tab)

    except:
        pass
    return result


def home(request, **kwargs):
# DEBUG
    # print(request.GET, request.POST)
    currentDatetime = datetime.datetime.now()
    searchDatetime = currentDatetime
    currentDate = currentDatetime.date()
    searchDate = currentDate
    currentTime = currentDatetime.time()
    searchTime = currentTime

    searchResult = None
    searchText = ""
    shouldSearch = True

    displayMode = {"current": None}
    courses_lec = coursescotty.CourseList()
    courses_sec = coursescotty.CourseList()
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
    catalog_semester = ""
    catalog_date = ""

    if request.method == "GET":
        data = dict(request.GET)

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

            if coursescotty.getSearchable(searchTextWithoutTime) == []:
# TODO needs to change the displayMode according to search date
                del displayMode["search"]
                searchResult = catalogsearcher_es.getCurrentCourses(current_datetime=searchDatetime)
            else:
                shouldSearch, mainpage_toast = catalogsearcher_es.presearch(searchTextWithoutTime)
                if shouldSearch:
                    searchResult = catalogsearcher_es.search(searchTextWithoutTime)

        else:
            searchResult = catalogsearcher_es.getCurrentCourses(current_datetime=searchDatetime)

    # put courses into lectures and sections
    if isinstance(searchResult, dict):
        try:
            courses_lec += searchResult["lectures"]
            courses_sec += searchResult["sections"]

            # dont forget to call ready
            courses_lec.ready(current_datetime=searchDatetime)
            courses_sec.ready(current_datetime=searchDatetime)
        except KeyError:
            pass

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
    catalog_semester = coursescotty.getCurrentSemester(searchResult)
    catalog_date = coursescotty.getCatalogDate(searchResult)

    context = {'searchText': searchText,
               'courses_lec': courses_lec,
               'courses_sec': courses_sec,
               'lecture_tab_text': lecture_tab_text,
               'section_tab_text': section_tab_text,
               'mainpage_toast': mainpage_toast,
               'displayMode': displayMode,
               'time_flags': time_flags,
               'search_tip': search_tip,
               'catalog_semester': catalog_semester,
               'catalog_date': catalog_date,
               'coursereview_year': (currentDate.year - 1)}

    return render(request, 'app/index.html', context)


def about(request):
    context = dict()
    return render(request, 'app/about.html', context)


def disclaimer(request):
    context = dict()
    return render(request, 'app/disclaimer.html', context)
