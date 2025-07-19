from django.db import models
from users.models import UserModel

class ProductModelCategory(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category


class ProductsModel(models.Model):
    salesman = models.ForeignKey(UserModel, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(ProductModelCategory, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    create_ad = models.DateTimeField(auto_now_add=True)
    update_ad = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title