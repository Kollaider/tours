import os

from django.shortcuts import render
from django.views import View

from django.http import HttpResponseNotFound

from data import tours, departures, title, subtitle, description, picture

import random


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... 404!')


def custom_handler500(request):
    return HttpResponseNotFound('Ой, что то сломалось... 500!')


class MainView(View):

    def get(self, request):
        tours_for_main_page = []
        some_list = random.sample(list(tours), 6)
        for i in range(len(some_list)):
            tours[some_list[i]]['trancated_text'] = tours[some_list[i]]['description'][:90]+'...'
            tours_for_main_page.append(tours[some_list[i]])

        context = {'tours_for_main_page': tours_for_main_page,
                   'title': title,
                   'subtitle': subtitle,
                   'description': description,
                   'departures': departures,
                   'picture': picture
                   }
        print(os.path)
        return render(request, 'index.html', context=context)


class DepartureView(View):

    def get(self, request, departure):

        departure_from = {}
        departure_title = {}
        list_of_nights = []
        list_of_pricies = []
        suffix = ''
        departure_from[departure] = departures[departure]

        departure_title['from'] = departures[departure]

        list_of_tours = []
        for key, value in tours.items():
            if value['departure'] == departure:
                list_of_tours.append(value)
                list_of_nights.append(value['nights'])
                list_of_pricies.append(value['price'])

        amount = len(list_of_tours)

        if amount%10 in (2,3,4) and amount not in (12, 13, 14):
            suffix = 'а'
        elif amount%10 == 1 and amount != 11:
            suffix = ''
        else:
            suffix = 'ов'


        return render(request, 'departure.html', context={'list_of_tours': list_of_tours,
                                                          'departures': departures,
                                                          'departure_from': departure_from,
                                                          'departure_title': departure_title,
                                                          'price_min': min(list_of_pricies),
                                                          'price_max': max(list_of_pricies),
                                                          'nights_min': min(list_of_nights),
                                                          'nights_max': max(list_of_nights),
                                                          'amount': amount,
                                                          'suffix': suffix})


class TourView(View):

    def get(self, request, id):
        tours[id]['stars_in_symb'] = int(tours[id]['stars'])*'★'
        context = tours[id]
        return render(request, 'tour.html', context=context)
