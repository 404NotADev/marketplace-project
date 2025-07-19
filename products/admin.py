from django.contrib import admin

from .models import ProductsModel, ProductModelCategory


admin.site.register(ProductsModel)
admin.site.register(ProductModelCategory)