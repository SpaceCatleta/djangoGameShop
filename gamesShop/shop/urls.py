from django.urls import path
from . import views


app_name = "shop"
urlpatterns = [
    path("", views.index, name="index"),
    path("library/", views.library, name="library"),
path("<int:pk>/", views.GameDetailView.as_view(), name="detail"),
]