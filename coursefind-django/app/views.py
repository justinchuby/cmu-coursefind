from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from django.http import HttpResponse

import datetime
import re
import random

try:
    from . import catalogsearcher_es, coursescotty, CFsitemap
    from .utilities import *
except:
    import catalogsearcher_es, coursescotty, CFsitemap
    from utilities import *


def getText(display_mode, tab, event_list):
    result = None
    try:
        if "search" in display_mode:
            if ("room" not in display_mode and
                (tab == "lecture" or tab == "section")):
                if len(event_list) > 1:
                    result = "Found {} {}s.".format(len(event_list), tab)
                elif len(event_list) == 1:
                    result = "Found one {}.".format(tab)
                elif len(event_list) == 0:
                    result = "Oops. Can't find any {}. Try something else!".format(tab)
            if "time" in display_mode:
                result += " (at {})".format(display_mode["time"].strftime("%I:%M%p"))

        elif "time" in display_mode:
            displayTime = display_mode["time"].strftime("%H:%M")
            if tab == "lecture" or tab == "section":
                if len(event_list.current) > 1:
                    result = "There are {} {}s at {}."\
                        .format(len(event_list.current), tab, displayTime)
                elif len(event_list.current) == 1:
                    result = "One {} happening at {}."\
                        .format(tab, displayTime)
                elif len(event_list.future) > 0:
                    result = "There are {}s in an hour from {}."\
                        .format(tab, displayTime)
                elif len(event_list) == 0:
                    result = "No {} happening at {}. Take a break :D"\
                        .format(tab, displayTime)

        elif "current" in display_mode:
            if tab == "lecture" or tab == "section":
                if len(event_list.current) > 1:
                    result = "There are currently {} {}s happening."\
                        .format(len(event_list.current), tab)
                elif len(event_list.current) == 1:
                    result = "One {} happening at this time."\
                        .format(tab)
                elif len(event_list.future) > 0:
                    result = "There are {}s happening in an hour."\
                        .format(tab)
                elif len(event_list) == 0:
                    result = "No {} happening at this time. Take a break :D"\
                        .format(tab)

    except:
        pass
    return result


def home(request, **kwargs):
# DEBUG
    # print(request.GET, request.POST)
    currentDatetime = datetime.datetime.now()
    currentDate = currentDatetime.date()
    currentTime = currentDatetime.time()
    searchDatetime = currentDatetime
    searchDate = currentDate
    searchTime = currentTime
    searchDay = None

    searchResult = None
    searchText = ""

    displayMode = {"current": None}
    courses_lec = coursescotty.CourseList()
    courses_sec = coursescotty.CourseList()
    lecture_tab_text = ""
    section_tab_text = ""

    mainpage_toast = None
    SEARCH_TIPS = ("a course number '15-112'",
                   "name of an instructor",
                   "name of a course",
                   "a room 'DH2210'",
                   "a building 'Doherty'",
                   "a time '8:00am'",
                   "a day 'Monday'")
    search_tip = None
    catalog_semester = ""
    catalog_date = ""
    # Different time divisions
    TIME_FLAGS = [["current", "Now happening"],
                  ["future", "In an hour"],
                  ["laterToday", "Later today"],
                  ["past", "Ended"],
                  ["rest", "On other days"]]

    search_tip = "Try searching for " + random.choice(SEARCH_TIPS)

    searchIndex = kwargs.get("index")

    if request.method == "GET":
        data = dict(request.GET)

        # Searching
        if "q" in data:
            displayMode["search"] = None

            # Get the query text. Data["q"] should be a list.
            try:
                searchText = data["q"][0]
            except:
                pass
            searchTextWithoutTime = searchText

            # Filter out the time first
            match = re.search("(\d\d?:\d{2})([ap]m)?", searchText)
            if match:
                try:
                    searchTime = parseTime(match.group())
                    searchDatetime = datetime.datetime.combine(searchDate, searchTime)
                    displayMode["time"] = searchTime
                except:
                    print("ERROR Fail to parse time: '{}'".format(match.group()))
                # Delete time from search text
                searchTextWithoutTime = re.sub("(\d\d?:\d{2})([ap]m)?", " ", searchText)

            if coursescotty.getSearchable(searchTextWithoutTime) == []:
                del displayMode["search"]
                searchResult = catalogsearcher_es.getCurrentCourses(
                    current_datetime=searchDatetime,
                    index=searchIndex)

            else:
                presearchResult = catalogsearcher_es.presearch(searchTextWithoutTime)
                mainpage_toast = presearchResult.get("mainpage_toast")
                searchResult = catalogsearcher_es.search(
                    text=searchTextWithoutTime,
                    index=searchIndex)

        # Not searching. Display current courses.
        else:
            searchResult = catalogsearcher_es.getCurrentCourses(
                current_datetime=searchDatetime,
                index=searchIndex)

    # Put courses into lectures and sections
    try:
        courses_lec += searchResult["lectures"]
        courses_sec += searchResult["sections"]
        # Set searchDay if it exists in the raw query.
        try:
            _day = searchResult["raw_query"]["day"][0]
            if _day == 0:
                _day = 7  # iso format
            if _day != currentDate.isoweekday():
                searchDay = _day
        except: pass

        # Don't forget to call ready
        courses_lec.ready(current_datetime=searchDatetime, current_day=searchDay)
        courses_sec.ready(current_datetime=searchDatetime, current_day=searchDay)
    except (KeyError, TypeError) as e:
        print(formatErrMsg(e))
    except:
        pass

    # Generate the result prompt
    lecture_tab_text = getText(displayMode, "lecture", courses_lec)
    section_tab_text = getText(displayMode, "section", courses_sec)
    if len(courses_lec) == 0 and len(courses_sec) > 0:
        lecture_tab_text += " But sections are found."

    # Get current semester and rundate from search results.
    catalog_semester = coursescotty.getCurrentSemester(searchResult)
    catalog_date = coursescotty.getCatalogDate(searchResult)

    context = {'page': 'root',
               'searchText': searchText,
               'courses_lec': courses_lec,
               'courses_sec': courses_sec,
               'lecture_tab_text': lecture_tab_text,
               'section_tab_text': section_tab_text,
               'mainpage_toast': mainpage_toast,
               'displayMode': displayMode,
               'time_flags': TIME_FLAGS,
               'search_tip': search_tip,
               'catalog_semester': catalog_semester,
               'catalog_date': catalog_date,
               # 'coursereview_year': (currentDate.year - 1),
               'coursereview_year': 2015,
               'search_index': searchIndex,
               'search_result': searchResult,
               'search_day': searchDay
               }

    return render(request, 'app/index.html', context)


def redirect_to_home(request):
    return redirect('/')


def about(request):
    catalog_semester = coursescotty.getCurrentSemester()
    context = {
        'page': 'about',
        'catalog_semester': catalog_semester
        }
    return render(request, 'app/about.html', context)


def disclaimer(request):
    catalog_semester = coursescotty.getCurrentSemester()
    context = {
        'page': 'disclaimer',
        'catalog_semester': catalog_semester
        }
    return render(request, 'app/disclaimer.html', context)


def course_detail(request, **kwargs):
    course_index = kwargs.get("index")
    courseid = kwargs.get("courseid")
    search_index = None
    data = dict(request.GET)
    try:
        search_index = data.get("search_index")[0]
    except:
        pass
    try:
        course = catalogsearcher_es.getCourseByID(courseid, course_index)
        context = {
            'page': 'course_detail',
            'search_index': search_index,
            'course_index': course_index,
            'catalog_semester': course.semester_current,
            'catalog_date': course.rundate,
            'course': course
        }
        return render(request, 'app/course_detail.html', context)
    except AttributeError:
        pass
    raise Http404("No info about {} in {}".format(courseid, course_index))


def redirect_to_course_detail(request, **kwargs):
    courseid = kwargs.get("courseid")
    course_index = kwargs.get("index")
    new_courseid = courseid[:2] + '-' + courseid[2:]
    if course_index:
        return redirect('/{}/{}'.format(course_index, new_courseid))
    else:
        return redirect('/courses/{}'.format(new_courseid))


def page_not_found(request, **kwargs):
    data = dict(request.GET)
    previous_page = data.get("src")
    try:
        previous_page = previous_page[0]
    except:
        pass
    context = {
        'page': '404',
        'previous_page': previous_page
        }
    return render(request, 'app/404.html', context)


def sitemap(request, **kwargs):
    index = kwargs.get("index")
    output = CFsitemap.generateSitemap(index)
    if output:
        return HttpResponse(output, content_type="text/plain")
    raise Http404("No sitemap for /{}".format(index))
