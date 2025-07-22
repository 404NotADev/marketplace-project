from django.contrib import admin

from .models import UserModel,UserActionLog

# Register your models here.
admin.site.register(UserModel)
admin.site.register(UserActionLog)