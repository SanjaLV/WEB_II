from random import randint

from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, User
from django.shortcuts import render, redirect
from django.utils import translation, timezone
from django.utils.translation import gettext_lazy as _

from django.http import HttpResponseForbidden

# Create your views here.
from main.GameLogic import GENERATE_NEW_ITEM, LocalItem, ValidateItem, RemoveItem, EquipItem, ProcessLoots, SellLoot, doFilter
from main.models import Character, Item, Loot, Bid, AuctionLog


def set_language(request, code):
    translation.activate(code)
    request.session[translation.LANGUAGE_SESSION_KEY] = code
    return redirect('/')


def index(request, msg=""):
    if request.user.is_authenticated:

        current_user = request.user

        char, ok = Character.objects.get_or_create(user=current_user)

        context = {'char': char, 'user': current_user, 'msg': msg}

        return render(request, "game.html", context)
    else:
        return render(request, 'base.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def getFreeGold(request):
    if request.user.is_authenticated:
        current_user = request.user
        char = Character.objects.get(user=current_user)
        r = randint(1, 100)
        char.gold += r
        char.save()

        return index(request, "You have received " + str(r) + " gold.")
    else:
        return HttpResponseForbidden()


def getItem(request):
    if request.user.is_authenticated:
        current_user = request.user
        char = Character.objects.get(user=current_user)
        NewItem = Item.objects.get(pk=GENERATE_NEW_ITEM(char.pk))

        return index(request, "You have recived " + NewItem.item_name + ".")
    else:
        return HttpResponseForbidden()


def Inventory(request):
    if request.user.is_authenticated:

        current_user = request.user
        char = Character.objects.get(user=current_user)

        itemz = Item.objects.filter(character_id=char.pk)

        stats = [0, 0, 0, 0, 0, 0, 0]
        ilvl = 0

        LocalItems = []
        EqItem = [0, 0, 0, 0]

        for x in itemz:

            local_item = LocalItem(x)

            if (char.eq_armor == x or char.eq_helm == x or char.eq_weapon == x or char.eq_offhand == x):
                EqItem[x.item_tupe] = local_item
                ilvl += x.item_level
                for x in range(len(stats)):
                    stats[x] += local_item.stats[x]
            elif not x.used:
                LocalItems.append(local_item)

        context = {'user': current_user, 'ilvl': ilvl, 'stats': stats, 'items': LocalItems, 'eq_items': EqItem}
        return render(request, 'inventory.html', context=context)

    else:
        return HttpResponseForbidden()


def ItemSwitch(request, item_id):
    if request.user.is_authenticated:
        current_user = request.user
        char = Character.objects.get(user=current_user)

        item = Item.objects.get(pk=item_id)
        if not item:
            return Inventory(request)

        # check if it's equeped
        if char.eq_weapon == item:
            RemoveItem(char, 0)
        elif char.eq_helm == item:
            RemoveItem(char, 1)
        elif char.eq_armor == item:
            RemoveItem(char, 2)
        elif char.eq_offhand == item:
            RemoveItem(char, 3)
        else:
            if not ValidateItem(char, item):
                return HttpResponseForbidden()

            RemoveItem(char, item.item_tupe)
            EquipItem(char, item)

        return Inventory(request)



    else:
        return HttpResponseForbidden()


# main page for Auction




def Auction(request):
    ProcessLoots()

    if request.user.is_authenticated:

        loots, values = doFilter(request.COOKIES)

        print(request.COOKIES)
        print(loots)

        context = {'filter': values, 'loots': loots}

        return render(request, "BrowseAuction.html", context=context)

    else:
        return HttpResponseForbidden()


def AuctionActive(request):
    ProcessLoots()

    if request.user.is_authenticated:
        current_user = request.user
        char = Character.objects.get(user=current_user)

        loots = Loot.objects.filter(character_id=char.pk).filter(active=True)
        bets = Bid.objects.filter(character_id=char.pk)

        context = {'loots': loots, 'bets': bets}

        return render(request, 'auction_active.html', context=context)
    else:
        return HttpResponseForbidden()


def AuctionCreate(request):
    if request.user.is_authenticated:
        current_user = request.user
        char = Character.objects.get(user=current_user)

        items = Item.objects.filter(character_id=char.pk).filter(used=False)

        context = {'items': items}

        return render(request, 'auction_make.html', context=context)
    else:
        return HttpResponseForbidden()


def AuctionFed(request):
    ProcessLoots()

    if request.user.is_authenticated:
        currect_user = request.user
        char = Character.objects.get(user=currect_user)

        logs = AuctionLog.objects.filter(character_id=char)

        context = {'logs': logs}

        return render(request, 'auction_log.html', context=context)

    else:
        return HttpResponseForbidden()


def MakeLoot(request, item_id):
    if request.user.is_authenticated:

        current_user = request.user
        char = Character.objects.get(user=current_user)
        item = Item.objects.get(pk=item_id)
        if ValidateItem(char, item):

            this_loot = Loot.objects.create()
            this_loot.item_id = item
            this_loot.character_id = char
            this_loot.active = True
            if request.COOKIES['start_bet'] > 0:
                this_loot.biddable = True
                this_loot.next_bid = int(request.COOKIES['start_bet'])
            else:
                this_loot.biddable = False
            this_loot.buy_out = int(request.COOKIES['buy_out'])
            this_loot.end_time = timezone.now() + timezone.timedelta(hours=+24)

            this_loot.save()
            item.used = True
            item.save()

            return AuctionActive(request)

        else:
            return HttpResponseForbidden()

    else:
        return HttpResponseForbidden()


def BuyLoot(request, loot_id):
    ProcessLoots()

    if request.user.is_authenticated:

        Buyer = Character.objects.get(user=request.user)

        loot = Loot.objects.get(pk=loot_id)
        if not loot:
            # failed to buy race condition or smthing
            return Auction(request)

        if Buyer.gold < loot.buy_out:
            return Auction(request)

        SellLoot(Buyer, loot, loot.buy_out)

        return AuctionFed(request)

    else:
        return HttpResponseForbidden()


def RemoveLoot(request, loot_id):
    ProcessLoots()

    if request.user.is_authenticated:
        loot = Loot.objects.get(pk=loot_id)
        if not loot:
            return AuctionActive(request)

        bets = Bid.objects.filter(loot_id=loot)

        if bets:
            return AuctionActive(request)
        else:
            item = loot.item_id
            item.used = False
            item.save()
            loot.delete()
            return AuctionActive(request)

    else:
        return HttpResponseForbidden()


def MakeBet(request, loot_id):
    ProcessLoots()

    if request.user.is_authenticated:
        loot = Loot.objects.get(pk=loot_id)
        if not loot.biddable:
            return HttpResponseForbidden()

        new_bid = request.COOKIES['bet']

        if (not new_bid) or (new_bid < loot.next_bid):
            return Auction(request)

        char = Character.objects.get(user=request.user)

        if char.gold < new_bid:
            return HttpResponseForbidden()

        char.gold -= new_bid
        char.save()

        # remove previous bet

        prev_bet = Bid.objects.filter(loot_id=loot).filter(active=True)

        if prev_bet:
            prev_bet.active = False
            moneyBack = prev_bet.character_id
            moneyBack.gold += prev_bet.price
            prev_bet.save()
            moneyBack.save()

        # make new bet
        BET = Bid.objects.create()
        BET.loot_id = loot
        BET.character_id = char
        BET.active = True
        BET.price = loot.next_bid
        BET.save()

        loot.next_bid = (loot.next_bid + 1 + (new_bid // 3))
        loot.save()



    else:
        return HttpResponseForbidden()
