import json
from dataclasses import dataclass, field
from shopping_cart.item import Item
from shopping_cart.random_number_utils import RandomUtils
from shopping_cart.file_io import Fstream

@dataclass
class Cart:
    database_path: str
    isEmpty: bool = True
    isActive: bool = False
    id: str = field(init=False, default_factory=RandomUtils.generate_random_id)

    def get_all_items(self, verbose=0)->dict:
        """
        Reads and returns a has map with all the available items

        Args:
            if verbose is set to 1, it will print all the items.

        Returns:
            dict: a hash map with all the items in the database.
        """
        data_file = Fstream.load_json_files(self.database_path)

        if len(data_file.items()) > 0:
            self.isEmpty = False
            self.isActive = True

        try:
            if verbose == 1:
                Fstream.print_json_structure(data_file)
                return data_file
            else:
                return data_file

        except:
            raise ValueError("The value for the verbose as to be 0 or 1")

    def search_items(self, query: str)->list[Item]:
        """
        """
        data = Fstream.load_json_files(self.database_path)
        matching_items = []
        for item_id, item_data in data["Items"].items():
            item = Item(name=item_data["name"], type=item_data["type"], _price=item_data["price"], id=item_id)
            if query.lower() in item.search_string.lower():
                matching_items.append(item)

        if len(matching_items) == 0:
            print("Not items found")

        else:
            for item in matching_items:
                print(f"Found: {item.name} {item.type} ${item.price}")

        return matching_items

    def get_total_item_count(self)->int:
        """
        Returns the total number of items in the cart.

        Returns:
            int: The total number of items in the cart.
        """
        data = self.get_all_items()
        return len(data["Items"].items())

    def add_item_to_cart(self, item: Item):
        """
        Adds an item to the cart and updates the database.json file.

        Args:
            item (Item): The item to add to the cart.
        """
        data = self.get_all_items()

        new_item = {
            "name": item.name,
            "type": item.type,
            "price": item.price
        }

        data["Items"][item.id] = new_item

        with open(self.database_path, 'w') as file:
            json.dump(data, file, indent=4)

        self.isEmpty = False
        self.isActive = True

        print(f"Added {item.name} to the cart.")

    def remove_items_from_cart_by_query(self, query: str):
        """
        Removes all the instances of an item from the cart based on a query.

        Args:
            query (str): The search query to find the item to remove.
        """
        data = self.get_all_items()
        items_to_remove = []

        for item_id, item_data in data["Items"].items():
            if query.lower() in item_data["name"].lower() or query.lower() in item_data["type"].lower():
                items_to_remove.append(item_id)

        if not items_to_remove:
            print(f"No items found matching '{query}'")
            return

        for item_id in items_to_remove:
            item_name = data["Items"][item_id]["name"]
            del data["Items"][item_id]
            print(f"Removed {item_name} from the cart.")

        with open(self.database_path, 'w') as file:
            json.dump(data, file, indent=4)

        if not data["Items"]:
            self.isEmpty = True
            self.isActive = False

    def remove_items_from_cart_by_selection(self):
        """
        Removes the selected item by index.
        """

        data = self.get_all_items()
        items = []
        i = 1
        for item_id, item_data in data["Items"].items():
            items.append(item_id)
            print(f"{i}: {item_data}")
            i += 1
        try:
            usr_choice = int(input("Select the item to delete by number, example: 0: ")) - 1
        except:
            raise ValueError("You must select a valid number!")

        if usr_choice > len(items):
            print("Item not found!")
            return

        item_to_delete = items[usr_choice]
        item_name = data["Items"][item_to_delete]["name"]
        del data["Items"][item_to_delete]
        print(f"Removed {item_name} from the cart.")

        with open(self.database_path, 'w') as file:
            json.dump(data, file, indent=4)

        if not data["Items"]:
            self.isEmpty = True
            self.isActive = False

    def get_total_price_of_items(self)->float:
        """"
        Returns:
            float: the total price for all the items in the cart.
        """
        data = self.get_all_items()
        total_amount = 0

        for item_id, item_data in data["Items"].items():
            total_amount += data["Items"][item_id]["price"]

        return total_amount

    def empty_cart(self):
        """
        Clear all the items in the cart.
        """
        data = self.get_all_items()
        if len(data["Items"].items()) > 0:
            data = {"Items":{}}

            with open(self.database_path, 'w') as file:
                json.dump(data, file, indent=4)

            if not data["Items"]:
                self.isEmpty = True
                self.isActive = False
            print("The cart is empty")
        else:
            print("The cart is already empty")

