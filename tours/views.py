import random

from data import departures, description, picture, subtitle, title, tours
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views import View


def custom_handler404(request, exception):

    return HttpResponseNotFound('Ой, что то сломалось... 404!')


def custom_handler500(request):

    return HttpResponseNotFound('Ой, что то сломалось... 500!')


class MainView(View):

    def get(self, request):

        numbers_of_tours = 6
        random_tours = random.sample(list(tours.items()), numbers_of_tours)
        return render(request, 'index.html', {'title': title,
                                              'subtitle': subtitle,
                                              'description': description,
                                              'random_tours': random_tours,
                                              'departures': departures,
                                              'picture': picture})


class DepartureView(View):

    def get(self, request, departure):
        departure_from = {}
        departure_title = {}
        list_of_nights = []
        list_of_pricies = []
        suffix = ''
        departure_from[departure] = departures[departure]

        departure_title['from'] = departures[departure]

        tours_filtered = []
        for key, value in tours.items():
            if value['departure'] == departure:
                value['tour_id'] = key
                tours_filtered.append(value)
                list_of_nights.append(value['nights'])
                list_of_pricies.append(value['price'])

        amount = len(tours_filtered)

        if amount % 10 in (2, 3, 4) and amount not in (12, 13, 14):
            suffix = 'а'
        elif amount % 10 == 1 and amount != 11:
            suffix = ''
        else:
            suffix = 'ов'
        return render(request, 'departure.html', context={'tours_filtered': tours_filtered,
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

    def get(self, request, tour_id):
        """Docstring."""
        tours[tour_id]['stars_in_symb'] = int(tours[tour_id]['stars']) * '★'
        dep_from = departures[tours[tour_id]['departure']]
        return render(request, 'tour.html', context={'dep_from': dep_from[0].lower() + dep_from[1:],
                                                     'tour': tours[tour_id],
                                                     'departures': departures})
