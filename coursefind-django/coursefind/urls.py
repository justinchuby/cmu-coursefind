"""coursefind URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, handler404
import app.views

handler404 = 'app.views.page_not_found'

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^about[/]?', app.views.about),
    url(r'^disclaimer[/]?', app.views.disclaimer),
    # home page
    url(r'^(?P<index>(f|s|m1|m2)\d{2})[/]?$', app.views.home),
    # detail page, ex. 15-112
    url(r'^courses/(?P<courseid>\d{2}-\d{3})/(?P<index>(f|s|m1|m2)\d{2})[/]?$', app.views.course_detail),
    url(r'^courses/(?P<courseid>\d{2}-\d{3})[/]?$', app.views.course_detail),
    # detail page (redirect), ex. 15112
    url(r'^courses/(?P<courseid>\d{5})/(?P<index>(f|s|m1|m2)\d{2})[/]?$', app.views.redirect_to_course_detail),
    url(r'^courses/(?P<courseid>\d{5})[/]?$', app.views.redirect_to_course_detail),
    # legacy url
    url(r'^(?P<index>(f|s|m1|m2)\d{2})/(?P<courseid>\d{2}-\d{3})[/]?$', app.views.redirect_to_course_detail),
    url(r'^(?P<index>(f|s|m1|m2)\d{2})/(?P<courseid>\d{5})[/]?$', app.views.redirect_to_course_detail),
    # site map
    url(r'^sitemaps/sitemap-(?P<index>((f|s|m1|m2)\d{2})|all_courses)\.txt$', app.views.sitemap),
    # home page
    url(r'^[/]?$', app.views.home),
    url(r'^', app.views.redirect_to_home)
]
