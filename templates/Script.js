

var last_item = 0;



function ClickItem(id) {
    Item = Items[id];

    document.getElementById("item_name").innerText = Item.name;
    document.getElementById("str").innerText = Item.str;
    document.getElementById("dex").innerText = Item.dex;
    document.getElementById("vit").innerText = Item.vit;
    document.getElementById("dmg").innerText = Item.dmg;
    document.getElementById("arm").innerText = Item.arm;
    document.getElementById("dod").innerText = Item.dod;
    document.getElementById("crh").innerText = Item.crh;
    document.getElementById("ilvl").innerText = Item.ilvl;

    last_item = id;

}

function Equip(id) {
    str = "/game/items/eq/" + id;
    window.location.href=str;
}