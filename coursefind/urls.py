"""coursefind URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url, handler404
import main.views

handler404 = 'main.views.page_not_found'

urlpatterns = [
    url(r'^$', main.views.Home.as_view()),
    url(r'^search[/]?', main.views.Home.as_view()),
    url(r'^about[/]?', main.views.Home.as_view()),
    url(r'^disclaimer[/]?', main.views.Home.as_view()),
    url(r'^courses/(?P<courseid>\d{2}-\d{3})[/]?$', main.views.CourseDetails.as_view()),
    url(r'^courses/(?P<courseid>\d{2}-\d{3})/(?P<index>(f|s|m1|m2)\d{2})[/]?$', main.views.CourseDetails.as_view()),
    # legacy urls
    url(r'^(?P<index>(f|s|m1|m2)\d{2})/(?P<courseid>\d{2}-\d{3})[/]?$', main.views.redirect_to_course_detail),
    url(r'^(?P<index>(f|s|m1|m2)\d{2})/(?P<courseid>\d{5})[/]?$', main.views.redirect_to_course_detail),
    # site map
    url(r'^sitemaps/sitemap-(?P<index>((f|s|m1|m2)\d{2})|current)\.txt$', main.views.sitemap),
]
