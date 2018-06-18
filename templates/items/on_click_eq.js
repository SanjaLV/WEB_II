function ItemClick(id) {

    document.cookie = "id = " + id;

    str = "/game/items/eq/" + id;
    window.location.href=str;
}