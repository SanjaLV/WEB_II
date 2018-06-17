
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('game/freegold', views.getFreeGold, name='freegold'),
    path('game/getItem', views.getItem, name='getItem'),
    path('game/inventory', views.Inventory, name='inventory'),
    path('game/items/eq/<int:item_id>', views.ItemSwitch, name='itemswitch'),
    path('language/<slug:code>', views.set_language, name='set_language')
]