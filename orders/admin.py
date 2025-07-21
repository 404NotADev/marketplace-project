from django.contrib import admin

from .models import Order, OrderItem, OrderHistory, UserRating

# Register your models here.
# orders/admin.py


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email',)
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'old_status', 'new_status', 'changed_at')
    list_filter = ('new_status', 'changed_at')
    search_fields = ('order__id', 'order__user__email')


@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'successful_orders')
    search_fields = ('user__email',)
