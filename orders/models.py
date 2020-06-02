from django.db import models


#Ordering stuff ------------------------------------
#Toppings for pizzas or add ons to subs
class Topping(models.Model):
    name = models.CharField(max_length=50)
    #The price is 0 for toppings but not for sub stuff
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)

#Any non add on item (Pizza, Subs, Salads and Pasta)
class MainItem(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    toppings = models.ManyToManyField(Topping, related_name="toppings")
    large = models.BooleanField()
    toppingLimit = models.IntegerField(default=4)
    canHaveToppings = models.BooleanField(default=True)

class Order(models.Model):
    totalPrice = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    mainItems = models.ManyToManyField(MainItem, related_name="main_items")
    user = models.CharField(max_length=50)

class PlacedOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order")
    #Progess variable: 0 processing, 1 delivering, 2 delivered
    progress = models.IntegerField(default=0)

#Menu / admin database stuff -------------------------------
class Menu(models.Model):
    #Pizza menu, Sub menu, Topping menu, etc. 
    name = models.CharField(max_length=50)
    isPriceless = models.BooleanField(default=False)
    smallAndLarge = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class MenuOption(models.Model):
    #A pizza, topping, sub, etc.
    name = models.CharField(max_length=50)
    smallPrice = models.DecimalField(max_digits=4, decimal_places=2, default=9.99)
    largePrice = models.DecimalField(max_digits=4, decimal_places=2, default=9.99)
    smallOnly = models.BooleanField(default=False)
    largeOnly = models.BooleanField(default=False)
    canHaveToppings = models.BooleanField(default=True)
    toppingLimit = models.IntegerField(default=4)
    fromMenu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu")

    def __str__(self):
        #Display name and price
        displayVal = self.name + ": " + str(self.smallPrice)

        #Display only one price if there's no small or large
        if not self.smallOnly:
            displayVal += " (S), " + str(self.largePrice) + (" (L) ")
        
        return  displayVal
