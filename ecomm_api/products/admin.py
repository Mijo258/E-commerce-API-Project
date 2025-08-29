from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.D):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.D):
    list_display = ('name', 'category', 'price', 'stock_quantity')
    list_filter = ('category',)
    search_fields = ('name', 'description')