from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from .models import Menu, MenuOption, Order, PlacedOrder, MainItem, Topping
from .creationForm import SignUpForm, SignUpManager
from .classes.MenuManager import MenuManager
from .classes.OrderManager import OrderManager

# Login/sign up/user related code ---------------------------------------------------------
def index(request):


    return render(request, "index.html", {"user": "Logged out"})

#Common function that gets menu information to be displayed
def getMenuDataDict(username = None, msg = None):

    mm = MenuManager()

    menuData = mm.getMenuDataDict(username)

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

    signUpManager = SignUpManager()

    result = signUpManager.SignUp(request)

    if result["outcome"] == 0: #Not post method
        return render(request, "signUp.html", {"user": "Logged out", "form": SignUpForm()})
    elif result["outcome"] == 1: #Success
        return redirect('../login/')
    else: #Invalid form
        return render(request, "signUp.html", {"form": result["form"]})
        

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

    #Get username for the orders database
    username=getAuthenticatedUser(request)    

    mm = MenuManager()
    mm.addItem(username, itemSize, id, mainItemID)
    
    return redirect('/menu')

#Remove an item already in the cart. mainItemName is set for toppings
def removeItem(request, itemId, mainItemID=None):

    #Get username for the orders database
    username=getAuthenticatedUser(request)    

    mm = MenuManager()
    mm.removeItem(username, itemId, mainItemID)

    return redirect('/menu')

def clearOrder(request):
    
    #Get username
    username=getAuthenticatedUser(request)    

    om = OrderManager()
    om.clearOrder(username)

    return redirect('/menu')

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

    om = OrderManager()
    
    #Submit the order, and get one of 3 different return outcomes
    outcome = om.submitOrder(request, username, orderId)

    if outcome == 0: #Not logged in
        return render(request, "index.html", {"user": "Logged out"})
    elif outcome == 1: #No order exists
        return render(request, "menu.html", getMenuDataDict(username, "An order was already placed. Please wait for delivery."))
    else: #success
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

    #Call order function which returns dictionary of data
    om = OrderManager()
    return render(request, "placedOrders.html", om.removeOrder(request, placedOrderId))

