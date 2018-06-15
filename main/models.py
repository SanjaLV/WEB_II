from django.db import models

# Create your models here.


class Item(models.Model):
    item_level = models.IntegerField(default=0)
    item_tupe = models.IntegerField()
    item_rarity = models.IntegerField()


class Affix(models.Model):
    affix_tupe = models.IntegerField()
    affix_value = models.IntegerField()
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)



