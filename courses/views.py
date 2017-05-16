from django.shortcuts import render
from django.http import Http404
from django.views import View
import requests
import json

from shared.coursescotty import Course
from shared.config import *


class CourseDetailView(View):
    courseid = ''
    course_index = ''

    def get(self, request):
        r = requests.get(COURSE_API_BASE + '%s/%s/' % self.courseid, self.course_index)
        # TODO error handling
        r_dict = json.loads(r.json())
        if 'error' not in r_dict:
            course = Course(r_dict['course'])
            context = {
                'page': 'course_detail',
                'search_index': self.search_index,
                'course_index': self.course_index,
                'catalog_semester': course.semester_current,
                'catalog_date': course.rundate,
                'course': course
            }
            return render(request, 'app/course_detail.html', context)

        # TODO Add different error pages
        raise Http404("No info about {} in {}".format(self.courseid, self.course_index))
