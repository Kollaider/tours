from django.shortcuts import render
from django.views import View

from django.http import HttpResponseNotFound


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... 404!')


def custom_handler500(request):
    return HttpResponseNotFound('Ой, что то сломалось... 500!')


class MainView(View):

    def get(self, request):
        return render(request, 'index.html')


class DepartureView(View):

    def get(self, request, departure):
        return render(request, 'departure.html', context={'departure': departure})


class TourView(View):

    def get(self, request, id):
        return render(request, 'tour.html', context={'id': id})
