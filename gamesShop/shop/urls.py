from django.urls import path
from . import views


app_name = "shop"
urlpatterns = [
    path("", views.index, name="index"),
    path("library/", views.library, name="library"),
    path("chart/", views.chart, name="chart"),
    path("add-new/", views.addGame, name="add-new"),
    path("post-new/", views.AddGame.as_view(), name="post-new"),
    path("<int:pk>/", views.GameDetailView.as_view(), name="detail"),
    path("add-to-chart/<int:pk>/", views.AddGameToChart.as_view(), name="add-to-chart"),
    path("delete-from-chart/<int:pk>/", views.deleteFromChart, name="delete-from-chart"),
]