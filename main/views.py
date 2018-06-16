from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

# Create your views here.
def index(request):
    return HttpResponse(_("Hello Here!"))