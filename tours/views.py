from django.shortcuts import render
from django.views import View


class MainView(View):

    def get(self, request):
        return render(request, 'index.html')


class DepartureView(View):

    def get(self, request, departure):
        return render(request, 'departure.html', context={'departure': departure})


class TourView(View):

    def get(self, request, id):
        return render(request, 'tour.html', context={'id': id})
