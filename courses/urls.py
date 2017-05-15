from django.conf.urls import url
from . import views


app_name = 'courses'

urlpatterns = [
    url(r'^(?P<courseid>\d{2}-\d{3})/(?P<index>(f|s|m1|m2)\d{2})[/]?$', views.CourseDetailView.as_view()),
    url(r'^(?P<courseid>\d{2}-\d{3})[/]?$', views.CourseDetailView.as_view())
]
