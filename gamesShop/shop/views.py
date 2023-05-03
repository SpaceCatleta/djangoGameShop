from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    print('CATALOG')
    counter = int(request.session.get('num_visits', 0)) + 1
    request.session['num_visits'] = str(counter)
    request.session.modified = True

    context =  {'num_visits': f'{counter}',
                'admin': True}
    return render(request, "shop/index.html", {'context': context})


def library(request):
    print('LIBRARY')
    context = {}
    return render(request, "shop/library.html", {'context': context})