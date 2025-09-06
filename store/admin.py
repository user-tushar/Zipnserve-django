from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductGallery
import admin_thumbnails
# Register your models here.


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductAdmin (admin.ModelAdmin): #prepopulate the slug.
    list_display = ('product_name', 'price', 'stock', 'category', 'is_avilable', 'modified_date')
    prepopulated_fields = {'slug': ('product_name', )}
    inlines = [ProductGalleryInline]

'''
this will prepopulate category slug.
means :  it will accept slug url automatically we don't need to write it.
'''

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',) # this is used to edit the selected data on that display spot .
    list_filter = ('product', 'variation_category', 'variation_value') # this will add a filter section on the side of the main section.

admin.site.register(Product,ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)

