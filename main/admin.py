from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Item)
admin.site.register(Affix)
admin.site.register(Character)
admin.site.register(Loot)
admin.site.register(AuctionLog)
admin.site.register(Bid)
