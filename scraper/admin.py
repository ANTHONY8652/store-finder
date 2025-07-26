from django.contrib import admin
from .models import Product

@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'source_site', 'created_at', 'last_updated')
    search_fields = ('name', 'source_site', 'created_at')

# Register your models here.
