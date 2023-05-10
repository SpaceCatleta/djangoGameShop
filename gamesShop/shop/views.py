from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic, View

from .form import AddGameForm
from .models import GameDetail, UsersGames, UserChart, UserProfile




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


class AddGameToChart(View):
    def post(self, request, pk):
        chartGame = UserChart(user=request.user, game=GameDetail.objects.get(pk=pk))
        chartGame.save()
        return redirect(f'/shop/{pk}/')

def deleteFromChart(request, pk):
    chartGame = UserChart.objects.get(user=request.user.id, game=pk)
    chartGame.delete()
    return redirect(f'/shop/chart/')


def library(request):
    current_user = request.user
    gamesList = [userGame.game for userGame in UsersGames.objects.filter(user=current_user.id)]

    for game in gamesList:
        if len(game.description) > 300:
            game.description = game.description[:300]
    context = {}
    return render(request, "shop/library.html", {'context': context, 'games_list': gamesList})


def chart(request):
    current_user = request.user
    userProfile = UserProfile.objects.get(user=current_user.id)
    gamesList = [userGame.game for userGame in UserChart.objects.filter(user=current_user.id)]
    totalPrice = 0
    for game in gamesList:
        totalPrice += game.price
        if len(game.description) > 300:
            game.description = game.description[:300]
    context = { 'total_price': totalPrice , 'balance': userProfile.balance,
                'total': userProfile.balance - totalPrice,
                'is_enough_money': totalPrice <= userProfile.balance}
    return render(request, "shop/chart.html", {'context': context, 'games_list': gamesList})


class AddGame(View):
    def post(self, request):
        form = AddGameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/shop')
        else:
            print("POST INVALID FORM")

class GamesLibrary(View):
    def post(self, request):
        current_user = request.user
        userProfile = UserProfile.objects.get(user=current_user.id)
        userGamesInChart = UserChart.objects.filter(user=current_user.id)
        userGames = [value.game for value in userGamesInChart]

        totalPrice = 0
        for game in userGames:
            totalPrice += game.price
            UsersGames(user=current_user, game=game).save()

        for game in userGamesInChart:
            game.delete()

        userProfile.balance -= totalPrice
        userProfile.save()
        return redirect(f'/shop/chart/')

class UserView(View):

    def get(self, request):
        current_user = request.user
        userProfile = UserProfile.objects.get(user=current_user.id)
        context = {
            'username': current_user.username,
            'balance': userProfile.balance
        }
        return render(request, "shop/profile.html", {'context': context})
