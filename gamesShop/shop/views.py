from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View

from .form import AddGameForm, RegisterForm
from .models import GameDetail, UsersGames, UserChart, UserProfile

from django.contrib.auth import logout


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

    gamesList = GameDetail.objects.filter(is_deleted=False)
    for game in gamesList:
        if len(game.description) > 300:
            game.description = game.description[:300]
    context =  {'num_visits': f'{counter}',
                'admin': True}
    return render(request, "shop/index.html", {'context': context, 'games_list': gamesList})





class AddGameToChart(View):
    def post(self, request, pk):
        chartGame = UserChart(user=request.user, game=GameDetail.objects.get(pk=pk))
        chartGame.save()
        return redirect(f'/shop/{pk}/')

def deleteFromChart(request, pk):
    chartGame = UserChart.objects.get(user=request.user.id, game=pk)
    chartGame.delete()
    return redirect(f'/shop/chart/')

def loginRedirect(request):
    return redirect('/accounts/login')

def logoutRedirect(request):
    return redirect('/accounts/logout')

def signUp(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'shop/register.html', { 'form': form})

def library(request):
    current_user = request.user
    gamesList = [userGame.game for userGame in UsersGames.objects.filter(user=current_user.id)]
    clearGamesList = []
    for game in gamesList:
        if len(game.description) > 300:
            game.description = game.description[:300]
            if not game.is_deleted:
                clearGamesList.append(game)

    context = {}
    return render(request, "shop/library.html", {'context': context, 'games_list': clearGamesList})


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



# addGame.html
class AddGame(View):

    @staticmethod
    def addGamePage(request):
        return render(request, "shop/addGame.html", {})

    def post(self, request):
        form = AddGameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/shop')
        else:
            print("POST INVALID FORM")

    @staticmethod
    def updateGamePage(request, pk):
        gameDetail  = get_object_or_404(GameDetail, id=pk)
        gameDetail.release_date = str(gameDetail.release_date)
        print(gameDetail.release_date)
        print("==========================================")
        return render(request, "shop/addGame.html", {'gameDetail': gameDetail, 'is_update_form': True})

    @staticmethod
    def updateGame(request, pk):
        instance = GameDetail.objects.get(pk=pk)
        form = AddGameForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(f'/shop/{pk}')
        else:
            print("POST INVALID FORM")


def softDeleteGame(request, pk):
    gameDetail  = get_object_or_404(GameDetail, id=pk)
    gameDetail.is_deleted = True
    gameDetail.save()
    return redirect('/shop')


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


def logout_view(request):
    logout(request=request)
    return redirect('/')