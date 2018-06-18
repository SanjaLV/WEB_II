import datetime

from django.utils import timezone

from main.models import Item, Affix, Character, Loot, AuctionLog, Bid
from random import randint

# GAME CONSTANTS


# RARITY
NORMAL = 0  # (1-45)  45
MAGIC = 1  # (46-70) 34
RARE = 2  # (70-90) 25
LEGENDARY = 3  # (95-100) 5

# ITEMS
WEAPON = 0
HELM = 1
ARMOR = 2
OFF_HAND = 3

# NAMES

names = [
    ["Sword", "Axe", "Hammer", "Katana", "Dagger"],
    ["Mask", "Demonhead", "Corona", "Diadem", "Helm"],
    ["Main", "Plate", "Sacred Armor", "Shell"],
    ["Shield", "Orb"]
]

# AFFIX
AF_STRENGTH = 0
AF_DEXTERITY = 1
AF_VITALITY = 2
AF_DAMAGE = 3
AF_ARMOR = 4
AF_DODGE = 5
AF_CRITICAL_HIT = 6

affix_count = [2, 3, 4, 5]
possible_affixes = [
    [0, 1, 3, 6],
    [0, 1, 2, 4],
    [0, 1, 2, 4, 5],
    [0, 1, 2, 3, 4, 5, 6]
]

procs_range = [
    [1, 100],
    [1, 100],
    [1, 100],
    [10, 400],
    [1, 100],
    [1, 10],
    [1, 10]
]


def GET_NAME():
    dd = randint(0, 3)

    name = names[dd][randint(0, len(names[dd]) - 1)]

    return dd, name


def GENERATE_AFFIXES(pk, rarity, item_tupe):
    res = 0

    item = Item.objects.get(pk=pk)

    for x in range(affix_count[rarity] + randint(-1, 1)):
        this_affix = Affix.objects.create()
        this_affix.affix_tupe = possible_affixes[item_tupe][randint(0, len(possible_affixes[item_tupe]) - 1)]
        this_affix.item_id = item
        this_affix.affix_value = randint(procs_range[this_affix.affix_tupe][0], procs_range[this_affix.affix_tupe][1])
        res += (this_affix.affix_value - procs_range[this_affix.affix_tupe][0]) / (
                procs_range[this_affix.affix_tupe][1] - procs_range[this_affix.affix_tupe][0]) * 100

        this_affix.save()

    return int(res)


def GENERATE_NEW_ITEM(char_pk):
    new_i = Item.objects.create()

    new_i.character_id = Character.objects.get(pk=char_pk)

    rarity = randint(1, 100)

    if rarity <= 45:
        new_i.item_rarity = NORMAL
    elif rarity <= 70:
        new_i.item_rarity = MAGIC
    elif rarity <= 90:
        new_i.item_rarity = RARE
    else:
        new_i.item_rarity = LEGENDARY

    a, b = GET_NAME()

    new_i.item_tupe, new_i.item_name = a, b

    new_i.item_level = GENERATE_AFFIXES(new_i.pk, new_i.item_rarity, new_i.item_tupe)

    new_i.save()

    return new_i.pk


class LocalItem:
    def __init__(self, item):
        self.pk = item.pk
        self.name = item.item_name
        self.stats = [0, 0, 0, 0, 0, 0, 0]
        self.rarity = item.item_rarity
        self.ilvl = item.item_level
        self.tupe = item.item_tupe

        afxs = Affix.objects.filter(item_id=item.pk)
        for x in afxs:
            self.stats[x.affix_tupe] += x.affix_value


class LocalLoot:
    def __init__(self, loot):
        self.pk = loot.pk
        self.biddable = loot.biddable
        self.buy_out = loot.buy_out
        self.next_bid = loot.next_bid
        self.item_id = LocalItem(loot.item_id)

class LocalHistory:
    def __init__(self, AH):
        self.item = LocalItem(AH.item)
        self.pk = AH.pk
        self.time = AH.time
        self.bought = AH.bought
        self.price = AH.price

class LocalBet:
    def __init__(self,bet):
        self.pk = bet.pk
        self.loot_pk = bet.loot_id.pk
        self.active = bet.active
        self.next_bet = bet.loot_id.next_bid
        self.buy_out = bet.loot_id.buy_out
        self.item = LocalItem(bet.loot_id.item_id)


def ValidateItem(char, item, inUsed=True):
    if item.character_id != char:
        return False
    if item.used and inUsed:
        return False
    return True


def RemoveItem(char, item_tupe):
    if item_tupe == 0:
        item = char.eq_weapon
        char.eq_weapon = None
    elif item_tupe == 1:
        item = char.eq_helm
        char.eq_helm = None
    elif item_tupe == 2:
        item = char.eq_armor
        char.eq_armor = None
    else:
        item = char.eq_offhand
        char.eq_offhand = None

    if item:
        item.used = False
        item.save()

    char.save()


def RemoveActiveBet(loot):
    prev_bet = Bid.objects.filter(loot_id=loot).filter(active=True)
    if prev_bet:
        prev_bet = prev_bet[0]
        prev_bet.active = False
        moneyBack = prev_bet.character_id
        moneyBack.gold += prev_bet.price
        print(prev_bet.price)
        prev_bet.save()
        moneyBack.save()


def SellLoot(Buyer, loot, price):
    item = loot.item_id
    Seller = loot.character_id

    item.used = False
    item.character_id = Buyer
    item.save()

    auc_log = AuctionLog.objects.create()
    auc_log.character_id = Seller
    auc_log.time = timezone.now()
    auc_log.bought = False
    auc_log.price = price
    auc_log.item = item

    auc_log.save()

    auc_log = AuctionLog.objects.create()
    auc_log.character_id = Buyer
    auc_log.time = timezone.now()
    auc_log.bought = True
    auc_log.price = price
    auc_log.item = item

    auc_log.save()

    Seller.gold += price
    Buyer.gold -= price

    Seller.save()
    Buyer.save()

    RemoveActiveBet(loot)

    loot.delete()


def EquipItem(char, item):
    item.used = True
    if item.item_tupe == 0:
        char.eq_weapon = item
    elif item.item_tupe == 1:
        char.eq_helm = item
    elif item.item_tupe == 2:
        char.eq_armor = item
    else:
        char.eq_offhand = item

    item.save()
    char.save()


# TODO Move this task to Celery and sheldue it every 30 seconds
def ProcessLoots():
    loots = Loot.objects.all()

    time_now = timezone.now()

    for x in loots:
        if x.end_time < time_now:
            # TODO END LOOT
            pass


def doFilter(COOKIES):
    loots = Loot.objects.all()
    res = []

    values = {}

    try:
        values['max_price'] = 2 ** 31
        if 'max_price' in COOKIES:
            values['max_price'] = int(COOKIES['max_price'])
            print(values['max_price'])
    except:
        pass

    try:
        values['tupe'] = 69
        if 'tupe' in COOKIES:
            values['tupe'] = int(COOKIES['tupe'])
    except:
        pass

    try:
        values['ilvl'] = 0
        if 'ilvl' in COOKIES:
            values['ilvl'] = int(COOKIES['ilvl'])
    except:
        pass

    try:
        values['str'] = 0
        if 'str' in COOKIES:
            values['str'] = int(COOKIES['str'])
    except:
        pass

    try:
        values['dex'] = 0
        if 'dex' in COOKIES:
            values['dex'] = int(COOKIES['dex'])
    except:
        pass

    try:
        values['vit'] = 0
        if 'vit' in COOKIES:
            values['vit'] = int(COOKIES['vit'])
    except:
        pass

    try:
        values['dmg'] = 0
        if 'dmg' in COOKIES:
            values['dmg'] = int(COOKIES['dmg'])
    except:
        pass

    try:
        values['arm'] = 0
        if 'arm' in COOKIES:
            values['arm'] = int(COOKIES['arm'])
    except:
        pass

    try:
        values['dod'] = 0
        if 'dod' in COOKIES:
            values['dod'] = int(COOKIES['dod'])
    except:
        pass
    try:
        values['crh'] = 0
        if 'crh' in COOKIES:
            values['crh'] = int(COOKIES['crh'])
    except:
        pass
    for x in loots:

        item = LocalItem(x.item_id)

        ok = True

        if 'max_price' in COOKIES:
            if x.biddable:
                if x.next_bid > values['max_price']:
                    ok = False
            else:
                if x.buy_out > values['max_price']:
                    ok = False

        if 'tupe' in COOKIES:
            if (values['tupe'] != 69) and (item.tupe != values['tupe']):
                ok = False

        if 'ilvl' in COOKIES:
            if item.ilvl < values['ilvl']:
                ok = False
        if 'str' in COOKIES:
            if item.stats[0] < values['str']:
                ok = False
        if 'dex' in COOKIES:
            if item.stats[1] < values['dex']:
                ok = False
        if 'vit' in COOKIES:
            if item.stats[2] < values['vit']:
                ok = False
        if 'dmg' in COOKIES:
            if item.stats[3] < values['dmg']:
                ok = False
        if 'arm' in COOKIES:
            if item.stats[4] < values['arm']:
                ok = False
        if 'dod' in COOKIES:
            if item.stats[5] < values['dod']:
                ok = False
        if 'crh' in COOKIES:
            if item.stats[6] < values['crh']:
                ok = False
        if ok:
            y = LocalLoot(x)
            res.append(y)

    return res, values
