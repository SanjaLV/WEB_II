
var Items = {};



var last_item = 0;



function Display(id) {
    Item = Items[id];


    document.getElementById("display_name").innerText = Item.name;
    document.getElementById("display_ilvl").innerText = Item.ilvl;
    document.getElementById("display_str" ).innerText = Item.str;
    document.getElementById("display_dex" ).innerText = Item.dex;
    document.getElementById("display_vit" ).innerText = Item.vit;
    document.getElementById("display_dmg" ).innerText = Item.dmg;
    document.getElementById("display_arm" ).innerText = Item.arm;
    document.getElementById("display_dod" ).innerText = Item.dod;
    document.getElementById("display_crh" ).innerText = Item.crh;

    last_item = id;

}

