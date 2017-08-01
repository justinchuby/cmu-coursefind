from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.http import Http404
from django.http import HttpResponse
import requests


class Home(View):
    def get(self, request):
        return render(request, 'main/index.html')


class CourseDetails(View):
    def get(self, request, **kwargs):
        courseid = kwargs.get("courseid")
        course_index = kwargs.get("index")
        if course_index:
            r = requests.get('https://api.cmucoursefind.xyz/course/v1/course/{}/term/{}/'.format(courseid, course_index))
        else:
            r = requests.get('https://api.cmucoursefind.xyz/course/v1/course/{}/'.format(courseid))
        context = {'course': r.json().get('course')}
        return render(request, 'main/course_details.html', context)


def page_not_found(request):
    return render(request, 'main/index.html')


def redirect_to_course_detail(request, **kwargs):
    courseid = kwargs.get("courseid")
    course_index = kwargs.get("index")
    if (len(courseid) == 5):
        courseid = courseid[:2] + '-' + courseid[2:]
    if course_index:
        return redirect('/courses/{}/{}'.format(courseid, course_index),
                        permanent=True)


def sitemap(request, **kwargs):
    course_index = kwargs.get("index")
    r = requests.get('https://api.cmucoursefind.xyz/course/v1/list-all-courses/term/{}/'.format(course_index))
    print(course_index)
    courseids = r.json().get('courseids')

    if courseids:
        output = ''
        for courseid in courseids:
            output += "https://www.cmucoursefind.xyz/courses/{}/{}\n".format(
                courseid.strip(), course_index.strip())
        return HttpResponse(output, content_type="text/plain")
        
    raise Http404("No sitemap for /{}".format(course_index))
