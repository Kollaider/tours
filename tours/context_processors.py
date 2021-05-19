import data


def about_site(request):
    return {'title': data.title,
            'subtitle': data.subtitle,
            'description': data.description,
            'departures': data.departures,
            'picture': data.picture}
