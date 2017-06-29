from django.shortcuts import render
from django.views import View
import shared.utils


class About(View):
    def get(self, request):
        context = {
            'page': 'about',
            'current_semester': shared.utils.getCurrentSemester()
        }
        return render(request, 'main/about.html', context)


class Disclaimer(View):
    def get(self, request):
        context = {
            'page': 'disclaimer',
            'current_semester': shared.utils.getCurrentSemester()
        }
        return render(request, 'main/disclaimer.html', context)
