
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('game/freegold', views.getFreeGold, name='freegold'),
    path('game/getItem', views.getItem, name='getItem'),
]