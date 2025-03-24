from django.utils.html import format_html
from django.contrib import admin
from .models import ProductModel,Order,OrderItem,AdoptionRequest

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'details', 'product_name', 'price', 'product_photo_preview', 'category','images','created_at','updated_at')

    def product_photo_preview(self, obj):
        if obj.product_photos:  
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />',
                obj.product_photos.url
            )
        return "No Image"

    product_photo_preview.short_description = "Product Photo"  

admin.site.register(ProductModel, ProductAdmin),

class ordermodel (admin.ModelAdmin):
    list_display = ('user','address','created_at','total_price','status')
admin.site.register(Order),
admin.site.register(OrderItem),
admin.site.register(AdoptionRequest),
