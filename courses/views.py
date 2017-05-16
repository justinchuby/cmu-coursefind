from django.shortcuts import render
from django.http import Http404
from django.views import View
import requests
import json

from shared.coursescotty import Course
from shared.config import *


class CourseDetailView(View):

    def get(self, request, courseid, course_index=''):
        req = COURSE_API_BASE + '{}/{}'.format(courseid, course_index)
        print(courseid)
        print(req)
        print()
        response = requests.get(req)
        # TODO error handling
        response_dict = response.json()
        if 'error' not in response_dict:
            course = Course(response_dict['course'])
            context = {
                'page': 'course_detail',
                'search_index': None,
                'course_index': course_index,
                'catalog_semester': course.semester_current,
                'catalog_date': course.rundate,
                'course': course
            }
            return render(request, 'courses/course_detail.html', context)

        # TODO Add different error pages
        raise Http404("No info about {} in {}".format(courseid, course_index))
