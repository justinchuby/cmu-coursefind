from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<index>(f|s|m1|m2)\d{2})/(?P<courseid>\d{2}-\d{3})[/]?$', views.course_detail),
    url(r'^courses/(?P<courseid>\d{2}-\d{3})[/]?$', views.course_detail),
    url(r'^(?P<index>(f|s|m1|m2)\d{2})/(?P<courseid>\d{5})[/]?$', views.redirect_to_course_detail),
    url(r'^courses/(?P<courseid>\d{5})[/]?$', views.redirect_to_course_detail)
]
