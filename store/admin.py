from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','category','description','image']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','mobile_no','email']

@admin.register(Orders)
class orderAdmin(admin.ModelAdmin):
    list_display = ['product','customer','quantity','price']