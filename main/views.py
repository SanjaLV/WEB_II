from random import randint

from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, User
from django.shortcuts import render, redirect
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from django.http import HttpResponseForbidden

# Create your views here.
from main.GameLogic import GENERATE_NEW_ITEM, LocalItem, ValidateItem, RemoveItem, EquipItem
from main.models import Character, Item


def set_language(request,code):
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
