from django.shortcuts import render
from django.views import View
import datetime
import shared.utils


class Home(View):
    def get(self, request):
        return None


class About(View):
    def get(self, request):
        current_semester = \
            shared.utils.get_semester_from_date(datetime.date.today())
        context = {
            'page': 'about',
            'current_semester': current_semester
        }
        return render(request, 'main/about.html', context)


class Disclaimer(View):
    def get(self, request):
        current_semester = \
            shared.utils.get_semester_from_date(datetime.date.today())
        context = {
            'page': 'disclaimer',
            'current_semester': current_semester
        }
        return render(request, 'main/disclaimer.html', context)
