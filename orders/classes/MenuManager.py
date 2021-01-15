from ..models import Menu, MenuOption, Order, PlacedOrder, MainItem, Topping
from decimal import *

# Add or remove items from the menu


class MenuManager():

    def addItem(self, username, itemSize, id, mainItemID):
        if username == None:
            # If not logged in then use the anonymous user
            username = "Anonymous"

        # Get id from database here
        itemToAdd = MenuOption.objects.get(pk=id)

        currentOrder = None

        # Check if an order exists in the database yet for the user
        if Order.objects.filter(user=username).exists():
            currentOrder = Order.objects.get(user=username)
            print("Order exists. Adding onto it.")
        else:  # If not then create one
            currentOrder = Order.objects.create(user=username)
            print("Order doesn't exist. A new one was created for user: " + username)

        # Add to price and set the size
        newPrice = Decimal('0.00')

        if itemSize == 1:
            # currentOrder.mainItems.add
            itemToAdd.large = True
            newPrice = itemToAdd.largePrice
        else:
            itemToAdd.large = False
            newPrice = itemToAdd.smallPrice

        currentOrder.totalPrice = Decimal(currentOrder.totalPrice) + newPrice

        # Add the item here depending on the type.
        # Toppings
        if itemSize == 2:
            # Get the main item the topping is added to here
            if currentOrder.mainItems.filter(id=mainItemID).exists():
                currentMainItem = currentOrder.mainItems.get(id=mainItemID)
                toppingCount = currentMainItem.toppings.all().count()
                if toppingCount < currentMainItem.toppingLimit:
                    currentMainItem.toppings.create(
                        name=itemToAdd.name, price=newPrice)
        else:  # Main Item (Pizza or Sub)
            currentOrder.mainItems.create(name=itemToAdd.name, price=newPrice, large=(
                itemSize == 1), canHaveToppings=itemToAdd.canHaveToppings, toppingLimit=itemToAdd.toppingLimit)

        # Now the item should be added to the database
        currentOrder.save()

    def removeItem(self, username, itemId, mainItemID):
        # Get username for the orders database

        if username == None:
            # If not logged in then use the anonymous user
            username = "Anonymous"

        # Check if an order exists in the database yet for the user
        if Order.objects.filter(user=username).exists():
            currentOrder = Order.objects.get(user=username)

            if mainItemID == None:  # Remove regular item

                # Check if the pizza or main item exists first
                if currentOrder.mainItems.filter(id=itemId).exists():
                    currentMainItem = currentOrder.mainItems.get(id=itemId)
                    currentOrder.totalPrice -= currentMainItem.price
                    currentMainItem.delete()

            else:  # Remove topping

                # First check if the main item exists
                if currentOrder.mainItems.filter(id=mainItemID).exists():
                    currentMainItem = currentOrder.mainItems.get(id=mainItemID)
                    # Then check if the topping exists in that main item (i.e. sub or pizza)
                    if currentMainItem.toppings.filter(id=itemId).exists():
                        currentTopping = currentMainItem.toppings.get(
                            id=itemId)
                        currentOrder.totalPrice -= currentTopping.price
                        currentTopping.delete()
            # Save changes if necessary
            currentOrder.save()
        else:
            print("Order object doesn't exist")

    # Function commonly called for template data

    def getMenuDataDict(self, username):

        menuData = {

            "menus": Menu.objects.all(),
            "items": MenuOption.objects.all(),
            "cartUser": username,
            "user": username,
            "orderStatus": None
        }

        # If not logged in you can cjeck out the menu, but don't say logged in as anonymous.
        if username == "Anonymous":
            menuData["user"] = "Logged out"

        # Show user's current cart if it exists
        if username is not None:
            if Order.objects.filter(user=username).exists():
                orderToDisplay = Order.objects.get(user=username)
                menuData["cart"] = orderToDisplay
                menuData["cartMainItems"] = orderToDisplay.mainItems.all()

                # Show a placed order's status if it exists
                if PlacedOrder.objects.filter(order_id=orderToDisplay.id).exists():
                    menuData["orderStatus"] = PlacedOrder.objects.get(
                        order_id=orderToDisplay.id).progress

        return menuData
