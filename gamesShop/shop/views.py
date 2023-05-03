from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic

from .models import GameDetail




class GameDetailView(generic.DetailView):
    model = GameDetail
    template_name = "shop/gameDetail.html"
    context_object_name = "gameDetail"


def index(request):
    print('CATALOG')
    counter = int(request.session.get('num_visits', 0)) + 1
    request.session['num_visits'] = str(counter)
    request.session.modified = True

    gamesList = GameDetail.objects.all()

    context =  {'num_visits': f'{counter}',
                'admin': True}
    return render(request, "shop/index.html", {'context': context, 'games_list': gamesList})


def library(request):
    print('LIBRARY')
    context = {}
    return render(request, "shop/library.html", {'context': context})