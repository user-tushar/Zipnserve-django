from django.urls import path
from . import views

urlpatterns = [
    path('',views.fxnstore, name='store'),
    path('category/<slug:category_slug>/',views.fxnstore, name='items_by_category'), # here this path is what will shown in browser ulr  
    path('category/<slug:category_slug>/<slug:product_slug>/',views.fxnsingle_product, name='product_detail'), # fist <> <>  are for defining path url for this function


    # '''this url is for showing category wise product in  store .
    # if we click any of category , only that specific category items will open. and that is work of slug'''
    path('search/',views.fxnsearch, name= 'search'),
    path('submit_review/<int:product_id>/',views.submit_review, name= 'submit_review'),


]