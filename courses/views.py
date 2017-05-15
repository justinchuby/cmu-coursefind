from django.shortcuts import render
from django.views import View


class CourseDetailView(View):
    course_index = ''
    courseid = ''

    def get(self, request):
        context = {
            'page': 'course_detail',
            'search_index': None,
            'course_index': self.course_index,
            'courseid': self.courseid
        }
        return render(request, 'app/course_detail.html', context)
