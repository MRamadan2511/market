from django.contrib import admin

from .models import OrderStatus, Order, OrderItem

admin.site.register(OrderStatus)
admin.site.register(Order)
admin.site.register(OrderItem)

