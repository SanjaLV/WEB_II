from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, User
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

# Create your views here.
from main.models import Character


def index(request):

    if (request.user.is_authenticated):

        current_user = request.user

        char, ok = Character.objects.get_or_create(pk=current_user.pk)

        context = {'char': char, 'user': current_user}

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

