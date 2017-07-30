from django.shortcuts import render
from django.views import View


class Home(View):
    def get(self, request):
        return render(request, 'main/base.html')
