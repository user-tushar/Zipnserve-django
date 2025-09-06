from django.shortcuts import render,redirect
# from django.http import HttpResponse
from store.models import Product  # here we call the model from store .. and there all products are present by category wise.
from store.models import Product, ReviewRating

# Create your views here.

# def fxnlog(request):
#     return render (request,'Login.html')

# def fxnhome(request):
#     return render (request,'homepage/Home.html') # inside homepage folder Home.html .



def fxnhome(request):
    products = Product.objects.all().filter(is_avilable = True).order_by('created_date')
    
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id = product.id, status=True)

    context = {
        'products': products, # the key will be called in html.
        'reviews': reviews,
    }

    return render (request,'Home.html',context)