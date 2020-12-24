from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

app_name="orders"
urlpatterns = [
    path("", views.index, name="index"),
    path('login/', LoginView.as_view(template_name='index.html'), name="login"),
    path('signUp/', views.signUp, name='signUp'),
    path('logOut/', views.view_logout, name='view_logout'),
    path('menu/', views.view_menu, name='view_menu'),
    path('addItem/<int:itemSize>/<int:id>/<int:mainItemID>/', views.addItem, name='addItem'),
    path('removeItem/<int:itemId>/<int:mainItemID>/', views.removeItem, name='removeItem'),
    path('removeItem/<int:itemId>/', views.removeItem, name='removeItem'),
    path('clearOrder/', views.clearOrder, name='clearOrder'),
    path('showCheckout/', views.showCheckout, name='showCheckout'),
    path('submitOrder/<int:orderId>', views.submitOrder, name='submitOrder'),
    path('admin/placedOrders', views.showPlacedOrders, name='showPlacedOrders'),
    path('admin/removeOrder/<int:placedOrderId>', views.removeOrder, name='removeOrder'),

]
