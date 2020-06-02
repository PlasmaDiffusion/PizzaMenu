from django.contrib import admin

from .models import  Menu, MenuOption, PlacedOrder


class MenuOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'fromMenu', 'smallPrice', 'largePrice', 'smallOnly')

admin.site.register(Menu)
admin.site.register(MenuOption, MenuOptionAdmin)
admin.site.register(PlacedOrder)