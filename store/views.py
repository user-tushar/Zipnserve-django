from django.shortcuts import render,get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
from django.http import Http404


# Create your views here.
def fxnstore(request, category_slug = None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category , slug= category_slug)
        products = Product.objects.filter(category = categories, is_avilable = True)
        paginator = Paginator(products, 5) # this 3 is for paginator
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count  = products.count()
    else:
        products = Product.objects.all().filter(is_avilable = True).order_by('id')
        paginator = Paginator(products, 15) # this 3 is for paginator
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count  = products.count() # this is to display dynamically product count in store page

    context = {
        'products': paged_products, # the key will be called in html.
        'product_count': product_count,
    }
    return render (request,'store.html',context)


def fxnsingle_product(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug , slug = product_slug) # here (__) double underscore is used for accessing to the slug inside category
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product = single_product).exists() #imported _cart_id & cartItem
    except Product.DoesNotExist:
        raise Http404("Product not found")
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id = single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
    
    reviews = ReviewRating.objects.filter(product_id = single_product.id, status=True)

    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_prodt' :single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }

    return render (request,'single_product.html',context)

def fxnsearch(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains = keyword)) # search product will display if the search keyword will be in discriptions OR product name of any product.
            # Q is stands for queryset for complex queries just like (|),(or) operator  AND  (and),(&) operator . we have to import it first from django.
            product_count  = products.count() # this is for count the product 

    context = {
        'products': products,
        'product_count': product_count,

    }
    return render (request,'store.html',context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id = request.user.id, product__id = product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Your review has been submitted.')
                return redirect(url)