import random

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views import View

from data import departures, tours


def custom_handler404(request, exception):

    return HttpResponseNotFound('Ой, что то сломалось... 404!')


def custom_handler500(request):

    return HttpResponseNotFound('Ой, что то сломалось... 500!')


class MainView(View):
    """The main page of the site"""

    def get(self, request):

        numbers_of_tours = 6
        random_tours = random.sample(list(tours.items()), numbers_of_tours)
        return render(request, 'index.html', {'random_tours': random_tours})


class DepartureView(View):
    """Display of tour directions."""

    def get(self, request, departure):

        if departure not in departures:
            return HttpResponseNotFound(f'Направление с именем {departure} нам не известено')

        list_of_nights = [value['nights'] for value in tours.values() if value['departure'] == departure]
        list_of_prices = [value['price'] for value in tours.values() if value['departure'] == departure]
        tours_filtered = {key: value for key, value in tours.items() if value['departure'] == departure}

        amount = len(tours_filtered)
        if amount % 10 in (2, 3, 4) and amount not in (12, 13, 14):
            suffix = 'а'
        elif amount % 10 == 1 and amount != 11:
            suffix = ''
        else:
            suffix = 'ов'

        return render(request, 'departure.html', context={'tours_filtered': tours_filtered,
                                                          'departure_name': departures[departure],
                                                          'price_min': min(list_of_prices),
                                                          'price_max': max(list_of_prices),
                                                          'nights_min': min(list_of_nights),
                                                          'nights_max': max(list_of_nights),
                                                          'suffix': suffix})


class TourView(View):
    """Display of the selected tour page."""

    def get(self, request, tour_id):

        if tour_id not in tours:
            return HttpResponseNotFound(f'Тур с id {tour_id} нам не известен')

        tours[tour_id]['stars_in_symb'] = int(tours[tour_id]['stars']) * '★'
        dep_from = departures[tours[tour_id]['departure']]

        return render(request, 'tour.html', context={'dep_from': dep_from[0].lower() + dep_from[1:],
                                                     'tour': tours[tour_id]})
