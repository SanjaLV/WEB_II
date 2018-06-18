
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('game/freegold', views.getFreeGold, name='freegold'),
    path('game/getItem', views.getItem, name='getItem'),
    path('game/inventory', views.Inventory, name='inventory'),
    path('game/items/eq/<int:item_id>', views.ItemSwitch, name='itemswitch'),
    path('language/<slug:code>', views.set_language, name='set_language'),
    path('auction/', views.Auction, name='auction'),
    path('auction/my', views.AuctionActive, name='active_auction'),
    path('auction/create', views.AuctionCreate, name='create_auction'),
    path('auction/log', views.AuctionFed, name='log_auction'),
    path('auction/create/<int:item_id>', views.MakeLoot, name='create_loot'),
    path('auction/buy/<int:loot_id>', views.BuyLoot, name='buy_loot'),
    path('auction/remove/<int:loot_id>', views.RemoveLoot, name='remove_loot'),
    path('auction/bet/<int:loot_id>', views.MakeBet, name='make_bet')

]