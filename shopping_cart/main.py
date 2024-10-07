from shopping_cart.item import Item
from shopping_cart.cart import Cart

if __name__ == "__main__":

    #the main database for the cart to pass to the class
    database = "./database.json"
    my_cart = Cart(database)

    #search for an item
    print("Searching item...")
    results = my_cart.search_items("apple")
    print("------------------------")

    #get the total amount of items in the cart
    print("Total items in the current cart:")
    total_item_count = my_cart.get_total_item_count()
    print(f"Total items count: {total_item_count}")

    print("------------------------")

    #Create an Item object so it can be added to the cart
    print("Adding items to the cart:...")
    print("------------------------")
    milk = Item("milk","liquid",1.23)
    my_cart.add_item_to_cart(milk)
    onion = Item("onion", "vegetable", 0.43)
    my_cart.add_item_to_cart(onion)

    #get all the items in the cart
    print("------------------------")
    print("Getting all the items in the cart:")
    print("------------------------")
    my_cart.get_all_items(verbose=1)

    print("------------------------")

    #remove all items by name or type
    print("Removing all instances of an item:")
    print("------------------------")
    my_cart.remove_items_from_cart_by_query("milk")
    print("------------------------")
    print("\n")
    #removes a selected item
    print("Removing a specific item by selection:")
    print("------------------------")
    my_cart.remove_items_from_cart_by_selection()
    print("------------------------")

    print("All the current items in the cart:")
    my_cart.get_all_items(verbose=1)
    print("------------------------")

    print("Total price for all the items in the cart:")
    total_price = my_cart.get_total_price_of_items()
    print(f"${total_price}")
