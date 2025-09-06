from django.urls import path
from . import views

# write your urls 
urlpatterns = [
    # path('',views.fxnlog),
    path('',views.fxnhome,name='Home'),
    # path('',views.fxnhome),


]