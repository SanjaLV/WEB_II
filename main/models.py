from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Character(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True),
    gold = models.BigIntegerField(default=0)


class Item(models.Model):
    item_name = models.CharField(max_length=30,null=True)
    item_level = models.IntegerField(default=0)
    item_tupe = models.IntegerField()
    item_rarity = models.IntegerField()
    character_id = models.ForeignKey(Character, on_delete=models.SET_NULL,null=True)

class Affix(models.Model):
    affix_tupe = models.IntegerField()
    affix_value = models.IntegerField()
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)




class Loot(models.Model):
    character_id = models.ForeignKey(Character, on_delete=models.SET_NULL,null=True)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    buy_out = models.IntegerField()
    next_bid = models.IntegerField()
    biddable = models.BooleanField()
    end_time = models.DateTimeField()

class Bid(models.Model):
    character_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    loot_id = models.ForeignKey(Loot, on_delete=models.CASCADE)
    active = models.BooleanField()
    price = models.IntegerField()


class AuctionLog(models.Model):
    character_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    time = models.DateTimeField()
    bought = models.BooleanField()
    price = models.IntegerField()




