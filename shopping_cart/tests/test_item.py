from shopping_cart.item import Item

def test_item_price()->None:
    item = Item("Car","vehicle",1200.02)
    assert item.price >= 0.0 or item.price == 1200.02

def test_item_name()->None:
    item = Item("a", "b", 16.00)
    assert len(item.name) > 0
