from django.urls import path
from . import views


app_name = "shop"
urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.UserView.as_view(), name="profile"),
    path("library/", views.library, name="library"),
    path("chart/", views.chart, name="chart"),

    path("add-new/", views.AddGame.addGamePage, name="add-new"),
    path("post-new/", views.AddGame.as_view(), name="post-new"),
    path("update-game-page/<int:pk>", views.AddGame.updateGamePage, name="update-game-page"),
    path("update-game/<int:pk>", views.AddGame.updateGame, name="update-game"),


    path("purchase/", views.GamesLibrary.as_view(), name="purchase"),
    path("<int:pk>/", views.GameDetailView.as_view(), name="detail"),
    path("add-to-chart/<int:pk>/", views.AddGameToChart.as_view(), name="add-to-chart"),
    path("delete-from-chart/<int:pk>/", views.deleteFromChart, name="delete-from-chart"),

path("logout/", views.logout, name="logout"),
]