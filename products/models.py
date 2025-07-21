from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductModelCategory(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category

class ProductsModel(models.Model):
    salesman = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(ProductModelCategory, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    create_ad = models.DateTimeField(auto_now_add=True)
    update_ad = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comments')
    product = models.ForeignKey(ProductsModel,on_delete=models.CASCADE,  related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True) 
    
    def __str__(self):
        return f'Коменнтарии от{self.user.email}на{self.product.title}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE, related_name='likes')
    def __str__(self):
        return f'{self.user.email} нравится {self.product.title}'

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite')
    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE, related_name='favorite')
    def __str__(self):
        return f'{self.user.email} добавил в избранные {self.product.title}'