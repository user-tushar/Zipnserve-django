from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html


# Register your models here.

class AccountAdmin(UserAdmin): 
    list_display = ('email','first_name', 'last_name', 'username', 'last_login', 'is_active', 'date_joined') # this is for display data we want to display in front of accounts pannel section.
    list_display_links = ('email','first_name', 'last_name') # these fields are use as link.
    # by default only one object is assigned as link from django model.
    # and here that is is 'email' since we set .. object name will display as email .. by the help of __str__ method in models.py
    # which is our main object name assigned as link ... but here we assigned (email,first_name,last_name) as link also.

    readonly_fields = ('last_login','date_joined') # these fields only we can read.

    ordering = ('-date_joined',) # this will display date_joined in descending ordering way .. the last one who joined will be in first.


    # these are the parms which is necessary before register the 'AccountAdmin' 
    filter_horizontal = ()
    list_filter = ()
    fieldsets =() 

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail (self, object):
        return format_html('<img src="{}" width="30" style="border-radius: 50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'profile_picture'
    list_display = ('thumbnail','user', 'city', 'state', 'country')
    


    
admin.site.register(Account,AccountAdmin) #and register the AccountAdmin here.
admin.site.register(UserProfile, UserProfileAdmin)