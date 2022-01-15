from django.contrib import admin, messages
from order.models import Order, OrderDetail


def Mark_as_Pending(modeladmin, request, queryset):
    queryset.update(order_status='Pending')
    messages.success(request, 'selected record(s) marked as Pending')

def Mark_as_Inprogress(modeladmin, request, queryset):
    queryset.update(order_status='Inprogress')
    messages.success(request, 'selected record(s) marked as Inprogress')

def Mark_as_Delivered(modeladmin, request, queryset):
    queryset.update(order_status='Delivered')
    messages.success(request, 'selected record(s) marked as Delivered')

def Mark_as_Cancelled(modeladmin, request, queryset):
    queryset.update(order_status='Cancelled')
    messages.error(request, 'selected record(s) marked as Cancelled')



class OrderDetailsInline(admin.TabularInline):
    model = OrderDetail
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'date_time', 'order_status', 'payment_status']
    list_filter = ['order_status', 'payment_status']
    date_hierarchy = 'date_time'
    actions = [Mark_as_Pending, Mark_as_Inprogress, Mark_as_Delivered, Mark_as_Cancelled]
    inlines = [OrderDetailsInline]

admin.site.register(Order, OrderAdmin)
