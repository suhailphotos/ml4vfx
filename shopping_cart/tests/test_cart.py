import pytest
from shopping_cart.cart import Cart
from shopping_cart.item import Item

@pytest.fixture
def cart():
    database = "./tests/test_database.json"
    cart = Cart(database)
    cart.empty_cart()
    return cart

def test_total_price_of_cart(cart):
    item1 = Item("apple", "fruit", 2.0)
    item2 = Item("pineapple", "fruit", 2.0)
    cart.add_item_to_cart(item1)
    cart.add_item_to_cart(item2)
    assert cart.get_total_price_of_items() == 4.0

def test_empty_cart(cart):
    item = Item("a", "b", 1.2)
    cart.add_item_to_cart(item)
    cart.empty_cart()
    assert len(cart.get_all_items()["Items"].items()) == 0

def test_search_item(cart):
    item = Item("tomato", "vegetable", 0.2)
    cart.add_item_to_cart(item)
    items_list = cart.search_items("tomato")
    assert items_list[0].name == "tomato"

def test_get_all_items(cart):
    item1 = Item("apple", "fruit", 2.0)
    item2 = Item("pineapple", "fruit", 2.0)
    cart.add_item_to_cart(item1)
    cart.add_item_to_cart(item2)
    retrieved_items = cart.get_all_items()
    names_to_compare = [item1.name, item2.name]
    results = [item_data["name"] for item_id, item_data in retrieved_items["Items"].items()]
    assert names_to_compare == results

def test_get_total_item_count(cart):
    item1 = Item("apple", "fruit", 2.0)
    item2 = Item("pineapple", "fruit", 2.0)
    cart.add_item_to_cart(item1)
    cart.add_item_to_cart(item2)
    assert cart.get_total_item_count() == 2
