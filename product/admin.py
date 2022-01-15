from django.contrib import admin, messages
from product.models import ProductCategory, Product, ProductImage, ProductImage


def activeStatus(modeladmin, request, queryset):
    queryset.update(status=True)
    messages.success(request, 'selected record(s) marked as active')

def inactiveStatus(modeladmin, request, queryset):
    queryset.update(status=False)
    messages.success(request, 'selected record(s) marked as inactive')

# Product Category Admin config
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
    list_filter = ('status', )
    search_fields = ('name', )
    actions = (activeStatus, inactiveStatus)

admin.site.register(ProductCategory, ProductCategoryAdmin)


# Product admin config

class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    extra = 1
    classes = ('collapse', )
    
# class ProductImageAdmin(admin.StackedInline):
#     model = ProductImage
#     extra = 1
#     classes = ('collapse', )



class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'product_category', 'stock', 'status']
    list_filter = ['product_category', 'status']
    search_fields = ['name', 'price']
    actions = [activeStatus, inactiveStatus]
    inlines = [ProductImageAdmin]

admin.site.register(Product, ProductAdmin)


