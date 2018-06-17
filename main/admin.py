from django.contrib import admin

# Register your models here.

from .models import Item
from .models import Affix
from .models import Character

admin.site.register(Item)
admin.site.register(Affix)
admin.site.register(Character)