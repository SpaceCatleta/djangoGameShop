from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic, View

from .form import AddGameForm
from .models import GameDetail, UsersGames, UserChart




class GameDetailView(generic.DetailView):
    model = GameDetail
    template_name = "shop/gameDetail.html"
    context_object_name = "gameDetail"

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        context['is_in_library'] = UsersGames.objects. \
            filter(user=self.request.user.id, game=int(self.get_object().id)).exists()
        context['is_in_chart'] = UserChart.objects.\
            filter(user=self.request.user.id,game=int(self.get_object().id)).exists()
        return context


def index(request):
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

def addToChart(request):
    return render(request, "shop/chart.html", {})

class AddGameToChart(View):
    def post(self, request, pk):
        chartGame = UserChart(user=request.user, game=GameDetail.objects.get(pk=pk))
        chartGame.save()
        return redirect(f'/shop/{pk}/')



def library(request):
    current_user = request.user

    gamesList = [userGame.game for userGame in UsersGames.objects.filter(user=current_user.id)]

    for game in gamesList:
        if len(game.description) > 300:
            game.description = game.description[:300]
    context = {}
    return render(request, "shop/library.html", {'context': context, 'games_list': gamesList})


class AddGame(View):
    def post(self, request):
        form = AddGameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/shop')
        else:
            print("POST INVALID FORM")