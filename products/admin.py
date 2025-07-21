from django.contrib import admin

from .models import ProductsModel, ProductModelCategory,Comment,Like,Favorite


admin.site.register(ProductsModel)
admin.site.register(ProductModelCategory)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Favorite)