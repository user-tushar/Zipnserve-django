from django.contrib import admin
from .models import Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin): #prepopulate the slug.
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name', 'slug' ) # this is for display data we want to display in front of accounts pannel section.
    
admin.site.register(Category, CategoryAdmin)


'''
{'key': value} --> dictonary
('data1','data2','data3') --> tuple
[data1, data2, data3] --> list
{data1, data2. data3} --> set

'''