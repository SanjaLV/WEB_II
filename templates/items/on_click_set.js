last_id = 0;

function ItemClick(id) {
    last_id = id;

    document.getElementById("item_id").innerText = Item[id].name;

}