from ..models import Menu, MenuOption, Order, PlacedOrder, MainItem, Topping
from decimal import *

#Submit orders, view orders (admin) and complete orders (admin)
class OrderManager():

    def clearOrder(self, username):
        if username == None:
            #If not logged in then use the anonymous user
            username = "Anonymous"

        #Remove order if it exists
        if Order.objects.filter(user=username).exists():
            currentOrder = Order.objects.get(user=username)
            currentOrder.delete()


    def submitOrder(self, request, username, orderId):
        if username == None:
            #If not logged in then do nothing
            return 0

        #Check if no placed orders exist
        if PlacedOrder.objects.filter(order_id=orderId).exists():
            return 1

        #Make a new order here if there isn't one already. Admins can view this.
        placedOrder = PlacedOrder.objects.create(order=Order.objects.get(pk=orderId))

        placedOrder.save()
        return 2


    def removeOrder(self, request, placedOrderId):
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

        return placedOrderDict
