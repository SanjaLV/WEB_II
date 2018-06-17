from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Character(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    gold = models.BigIntegerField(default=0)
    eq_weapon = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True, related_name="weapon")
    eq_helm   = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True, related_name="helm")
    eq_armor  = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True, related_name="armor")
    eq_offhand= models.ForeignKey('Item', on_delete=models.SET_NULL, null=True, related_name="offhand")



class Item(models.Model):
    item_name = models.CharField(max_length=30,null=True)
    item_level = models.IntegerField(default=0)
    item_tupe = models.IntegerField(null=True)
    item_rarity = models.IntegerField(null=True)
    character_id = models.ForeignKey(Character, on_delete=models.SET_NULL,null=True)
    used = models.BooleanField(default=False)

class Affix(models.Model):
    affix_tupe = models.IntegerField(null=True)
    affix_value = models.IntegerField(null=True)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)




class Loot(models.Model):
    character_id = models.ForeignKey(Character, on_delete=models.SET_NULL,null=True)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE,null=True)
    buy_out = models.IntegerField(default=0)
    next_bid = models.IntegerField(default=0)
    biddable = models.BooleanField(default=False)
    end_time = models.DateTimeField(null=True)

class Bid(models.Model):
    character_id = models.ForeignKey(Character, on_delete=models.CASCADE,null=True)
    loot_id = models.ForeignKey(Loot, on_delete=models.CASCADE,null=True)
    active = models.BooleanField(default=False)
    price = models.IntegerField(default=0)


class AuctionLog(models.Model):
    character_id = models.ForeignKey(Character, on_delete=models.CASCADE,null=True)
    time = models.DateTimeField(null=True)
    bought = models.BooleanField(default=False)
    price = models.IntegerField(default=0)




