Python Files:

views.py - Main code file with all functionality aside from editing the database

creationForm.py - Has a sign up class that uses a django form, with additional fields for first name, last name and email.

urls.py - URL paths to each view, including url arguments for getting data from the database.

models.py - Database models for dispalying the menu (Menu and MenuOption classes), and placing orders (Topping, MainItem, Order and PlacedOrder classes)

--------------------------------------------------
Template Files:

index.html - The main page prompting the user to login or sign up

signUp.html - Self explanatory 

layout.html - CSS reference to inherit from in other html files



menu.html - Where the user is directed upon logging in. They can add items to their cart here.

placedOrders.html - A page for admins/store owners only to see placed orders and mark them as delivering/delivered

checkout.html - Prompts the user to confirm an order, showing the prices and items in the cart

addTopping.html - Reusable code snippet that creates add topping items for pizzas/subs in your cart

addSmallhtml/addLargeItem.html- Reusable code snippet that creates buttons for adding non topping items


--------------------------------------------------
Static Files:
orders/static/styles - CSS file 

orders/static/images and aesthetic images
