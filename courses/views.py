from django.shortcuts import render
from django.http import Http404, HttpResponseServerError
from django.views import View
import requests

from shared.cmu_course import Course
import shared.config as config


class CourseDetailView(View):

    def get(self, request, courseid, course_index=None):
        if course_index is None:
            req = config.COURSE_API_BASE + 'course/{}/'.format(courseid)
        else:
            req = config.COURSE_API_BASE + 'course/{}/term/{}/'.format(courseid, course_index)
        print(courseid)
        print(req)
        print()
        response = requests.get(req)
        # TODO error handling
        response_dict = response.json()
        try:
            if 'error' not in response_dict:
                course = Course(response_dict['course'])
                context = {
                    'page': 'course_detail',
                    'search_index': None,
                    'course_index': course_index,
                    'catalog_semester': course.semester,
                    'catalog_date': course.rundate,
                    'course': course
                }
                return render(request, 'courses/course_detail.html', context)
        except TypeError:
            raise HttpResponseServerError()

        # TODO Add different error pages
        raise Http404("No info about {} in {}".format(courseid, course_index))
