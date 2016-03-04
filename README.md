# README #


## Introduction ##

The project I am working on is a course finder, **CourseFind**.

I had the idea one day when I was wandering in Wean Hall at CMU. I saw students having classes and hoped to find out what classes they were having. I could just walk in and see what was going on, but it would be much better if I knew something about the class.

With CourseFind, students can easily find out what’s going on in a class room. So they can explore what’s course is interests them. CourseFind is also great for finding the room for a class, or just browsing the catalog to find what’s interesting.


## How do I get set up? ##



* Configuration

    This website uses Django as the backend framework. Follow the instruction on [https://www.djangoproject.com/download/](Link URL) to install Django.

    To run the site locally, cd into the coursefind-django folder, and run

```
#!bash

$ python3 manage.py runserver
```

## Project Structure ##


```
├── app
│   ├── __init__.py
│   ├── catalogsearcher.py
│   ├── cmu_info.py
│   ├── cmu_prof.py
│   ├── coursecat.py
│   ├── models.py
│   ├── static
│   │   └── app ...
│   ├── templates
│   │   └── app
│   │       ├── about.html
│   │       ├── analytics.html
│   │       ├── course_list.html
│   │       ├── disclaimer.html
│   │       ├── index.html
│   │       ├── layout.html
│   │       └── meta_search.html
│   ├── templatetags
│   │   ├── __init__.py
│   │   └── template_filter.py
│   ├── tests.py
│   ├── utilities.py
│   └── views.py
├── coursefind
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
└── manage.py
```
