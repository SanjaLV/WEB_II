from random import randint

from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, User
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from django.http import HttpResponseForbidden

# Create your views here.
from main.GameLogic import GENERATE_NEW_ITEM
from main.models import Character, Item


def index(request, msg = ""):
    if request.user.is_authenticated:

        current_user = request.user

        char, ok = Character.objects.get_or_create(pk=current_user.pk)

        context = {'char': char, 'user': current_user, 'msg': msg}

        return render(request, "game.html",context)
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
        char = Character.objects.get(pk=current_user.pk)
        r = randint(1,100)
        char.gold += r
        char.save()

        return index(request, "You have received " + str(r) + " gold.")
    else:
        return HttpResponseForbidden()


def getItem(request):
    if request.user.is_authenticated:
        current_user = request.user
        char = Character.objects.get(pk=current_user.pk)
        NewItem = Item.objects.get(pk = GENERATE_NEW_ITEM(char.pk))

        return index(request, "You have recived " + NewItem.item_name + "." )
    else:
        return HttpResponseForbidden()

