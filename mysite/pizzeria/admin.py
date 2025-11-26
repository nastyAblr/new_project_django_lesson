
from django.contrib import admin
from .models import Pizza, Order

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'slug')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'pizza', 'created_at')
    list_filter = ('created_at', 'pizza')
    search_fields = ('name', 'phone', 'address')

# Register your models here.
