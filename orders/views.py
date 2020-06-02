from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from .models import Menu, MenuOption, Order, PlacedOrder, MainItem, Topping
from decimal import *
from .creationForm import SignUpForm
#from .classes.creationForm import SignUpForm

# Login/sign up/user related code ---------------------------------------------------------
def index(request):


    return render(request, "index.html", {"user": "Logged out"})

#Common function that gets menu information to be displayed
def getMenuDataDict(username = None, msg = None):


    menuData = {
        
        "menus": Menu.objects.all(),
        "items": MenuOption.objects.all(),
        "cartUser": username,
        "orderStatus": None
    }

    #Show user's current cart if it exists
    if username is not None:
        if Order.objects.filter(user=username).exists():
            orderToDisplay = Order.objects.get(user=username)
            menuData["cart"] = orderToDisplay
            menuData["cartMainItems"] = orderToDisplay.mainItems.all()
    
            #Show a placed order's status if it exists
            if PlacedOrder.objects.filter(order_id=orderToDisplay.id).exists():
                menuData["orderStatus"] = PlacedOrder.objects.get(order_id=orderToDisplay.id).progress
    

    #Show any extra message if set
    if msg is not None:
        menuData["msg"]= msg

    return menuData

#Common function to get the user and make sure they are logged in
def getAuthenticatedUser(request):
     
    if not request.user.is_authenticated:
        print("not authenticated")
        return None

    if request.user.is_anonymous:
        return None
    
    return request.user.username

#Uses the SignUpForm class to sign up a user. If the user enters valid data then they are added to the user database.
def signUp(request):

    print("\n \n \n")
    print("Signing up...")

    if request.method != 'POST':
        return render(request, "signUp.html", {"user": "Logged out", "form": SignUpForm()})
    

    form = SignUpForm(data=request.POST)
 
    username = "none :P"

    if form.is_valid():

        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        print("New user: " + username)
        user = authenticate(request, username=username, password=password)
        return redirect('../login/')
        #return render(request, "menu.html", getMenuDataDict(username))

    else:

        print("Form invalid...\n")
        
        return render(request, "signUp.html", {"form": form})

def view_logout(request):
    logout(request)
    return render(request, "index.html", {"msg": "Logged out."})

#Pizza Ordering code ------------------------------------------------------------  

#Show the menu by reading it from the database after login.
def view_menu(request):

    #Load menu here if it exists (From username)
    username=getAuthenticatedUser(request)    
    if username == None:
        #If not logged in then do nothing
        return render(request, "menu.html", getMenuDataDict("Anonymous"))

    #If a super user then give the option to display orders
    if request.user.is_superuser:
        return render(request, "menu.html", getMenuDataDict(username, "IsSuperUser"))
    

    return render(request, "menu.html", getMenuDataDict(username))

#Add an item to the cart. mainItemName is set for toppings
def addItem(request, itemSize, id, mainItemID):


    #Get id from database here
    itemToAdd = MenuOption.objects.get(pk=id)

    #Get username for the orders database
    username=getAuthenticatedUser(request)    
    if username == None:
        #If not logged in then use the anonymous user
        username = "Anonymous"

    currentOrder = None

    #Check if an order exists in the database yet for the user
    if Order.objects.filter(user=username).exists():
        currentOrder = Order.objects.get(user=username)
        print("Order exists. Adding onto it.")
    else: #If not then create one
        currentOrder = Order.objects.create(user=username)
        print("Order doesn't exist. A new one was created for user: " + username)


    #Add to price and set the size
    newPrice = Decimal('0.00')

    if itemSize == 1:
        #currentOrder.mainItems.add
        itemToAdd.large = True
        newPrice = itemToAdd.largePrice
    else:
        itemToAdd.large = False
        newPrice = itemToAdd.smallPrice

    currentOrder.totalPrice = Decimal(currentOrder.totalPrice) + newPrice

    #Add the item here depending on the type.
    #Toppings
    if itemSize == 2:
        #Get the main item the topping is added to here
        if currentOrder.mainItems.filter(id=mainItemID).exists():
            currentMainItem = currentOrder.mainItems.get(id=mainItemID)
            toppingCount = currentMainItem.toppings.all().count()
            if toppingCount < currentMainItem.toppingLimit:
                currentMainItem.toppings.create(name=itemToAdd.name, price=newPrice)
    else: #Main Item (Pizza or Sub)
        currentOrder.mainItems.create(name=itemToAdd.name, price=newPrice, large=(itemSize==1), canHaveToppings=itemToAdd.canHaveToppings, toppingLimit=itemToAdd.toppingLimit)

    #Now the item should be added to the database
    currentOrder.save()

    
    return redirect('/accounts/profile')

#Remove an item already in the cart. mainItemName is set for toppings
def removeItem(request, itemId, mainItemID=None):

    #Get username for the orders database
    username=getAuthenticatedUser(request)    
    if username == None:
        #If not logged in then use the anonymous user
        username = "Anonymous"

    #Check if an order exists in the database yet for the user
    if Order.objects.filter(user=username).exists():
        currentOrder = Order.objects.get(user=username)
        
        if mainItemID == None: #Remove regular item
            
            #Check if the pizza or main item exists first
            if currentOrder.mainItems.filter(id=itemId).exists():
                currentMainItem = currentOrder.mainItems.get(id=itemId)
                currentOrder.totalPrice -=  currentMainItem.price
                currentMainItem.delete()
            
        else: #Remove topping

            #First check if the main item exists
            if currentOrder.mainItems.filter(id=mainItemID).exists():
                currentMainItem = currentOrder.mainItems.get(id=mainItemID)
                #Then check if the topping exists in that main item (i.e. sub or pizza)
                if currentMainItem.toppings.filter(id=itemId).exists():
                    currentTopping = currentMainItem.toppings.get(id=itemId)
                    currentOrder.totalPrice -= currentTopping.price
                    currentTopping.delete()
        #Save changes if necessary
        currentOrder.save()
    else:
        print("Order object doesn't exist")

    return redirect('/accounts/profile')

def clearOrder(request):
    
    #Get username
    username=getAuthenticatedUser(request)    
    if username == None:
        #If not logged in then use the anonymous user
        username = "Anonymous"

    #Remove order if it exists
    if Order.objects.filter(user=username).exists():
        currentOrder = Order.objects.get(user=username)
        currentOrder.delete()

    return render(request, "menu.html", getMenuDataDict(username))

def showCheckout(request):
    #Get username
    username=getAuthenticatedUser(request)    
    if username == None:
        #If not logged in then do nothing
        return render(request, "index.html", {"user": "Logged out"})

    return render(request, "checkout.html", getMenuDataDict(username))

#Submit an order so admins will be able to see them and deliver them
def submitOrder(request, orderId):

    #Get username
    username=getAuthenticatedUser(request)    
    if username == None:
        #If not logged in then do nothing
        return render(request, "index.html", {"user": "Logged out"})

    #Check if no placed orders exist
    if PlacedOrder.objects.filter(order_id=orderId).exists():
        return render(request, "menu.html", getMenuDataDict(username, "An order was already placed. Please wait for delivery."))

    #Make a new order here if there isn't one already. Admins can view this.
    placedOrder = PlacedOrder.objects.create(order=Order.objects.get(pk=orderId))

    placedOrder.save()

    return render(request, "menu.html", getMenuDataDict(username, "Order Submitted!"))

#Admin can see and mark off placed orders with these views here ---------------------------------------------------
def showPlacedOrders(request):

    #Make sure superuser
    if request.user.is_authenticated:
        if request.user.is_superuser:

            #Get orders to send to the template  
            placedOrderDict = {
                "placedOrders": PlacedOrder.objects.all()
            }

            return render(request, "placedOrders.html", placedOrderDict)
            

    return render(request, "menu.html", getMenuDataDict())

def removeOrder(request, placedOrderId):

    #Make sure superuser
    if request.user.is_authenticated:
        if request.user.is_superuser:

            if PlacedOrder.objects.filter(id=placedOrderId).exists():
                orderToComplete = PlacedOrder.objects.get(id=placedOrderId)
                
                #First mark the order as pending. Then Delivering. Then Delivered.
                orderToComplete.progress += 1
                orderToComplete.save()
                #The third time this is called, delete the placed order.
                if orderToComplete.progress >= 2:
                    orderToComplete.delete()

    #Get orders to send to the template      
    placedOrderDict = {
        "placedOrders": PlacedOrder.objects.all()
    }

    return render(request, "placedOrders.html", placedOrderDict)

