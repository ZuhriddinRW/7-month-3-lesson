from django.contrib import admin
from .models import *


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'birth_date', 'created_at']
    search_fields = ['full_name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'birth_date', 'created_at']
    search_fields = ['full_name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'quantity', 'price', 'created_at']
    search_fields = ['name']


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'employee', 'total_price', 'order_date']
    list_filter = ['order_date']
    inlines = [OrderProductInline]


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price']