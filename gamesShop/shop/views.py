from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic, View

from .form import AddGameForm
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
    for game in gamesList:
        if len(game.description) > 300:
            game.description = game.description[:300]
    context =  {'num_visits': f'{counter}',
                'admin': True}
    return render(request, "shop/index.html", {'context': context, 'games_list': gamesList})


def addGame(request):
    return render(request, "shop/addGame.html", {})


def library(request):
    print('LIBRARY')
    context = {}
    return render(request, "shop/library.html", {'context': context})


class AddGame(View):
    def post(self, request):
        form = AddGameForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
        else:
            print("POST INVALID FORM")

        return redirect('/shop')