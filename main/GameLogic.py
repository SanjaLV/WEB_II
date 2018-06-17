from main.models import Item, Affix, Character
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


class LocalItem():
    def __init__(self, item):
        self.pk = item.pk
        self.name = item.item_name
        self.stats = [0, 0, 0, 0, 0, 0, 0]
        self.rarity = item.item_rarity
        self.ilvl = item.item_level

        afxs = Affix.objects.filter(item_id=item.pk)
        for x in afxs:
            self.stats[x.affix_tupe] += x.affix_value


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
