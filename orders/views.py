from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .models import Order,Payment,OrderProduct
from .forms import OrderForm
from store.models import Product,Variation

# mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Module
import datetime
import json



# Create your views here.


def fxnpayment(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number = body['orderID'])

    # store transation details inside Payment model.
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # move the cart items to order product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        # variations are applied on user purchasing product.
        cart_item = CartItem.objects.get(id = item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id =orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        # after purchased a product the quantity will be reduced from the admin pannel store as well
        product = Product.objects.get(id = item.product_id)
        product.stock -= item.quantity
        product.save()

    # After payment succefully .. clear the cart ..
    CartItem.objects.filter(user=request.user).delete()

    # send the order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('order_recieved_email.html',{
        'user': request.user,
        'order': order,
    })
    to_mail = request.user.Email
    send_mail = EmailMessage(mail_subject, message, to=[to_mail])
    send_mail.send()

    # sent order no & transation id  back to sendData thrugh JsonResponsoe to Paypal Js. 
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)

    # return render(request, 'payments.html')


def place_order(request, total=0, quantity = 0):
    current_user = request.user

    # if item in cart 0, redirect to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect ('store')
    
    grand_total = 0
    tax =0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (18 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():

            #  billing info got saved
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address1 = form.cleaned_data['address1']
            data.address2 = form.cleaned_data['address2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.pin = form.cleaned_data['pin']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR') # this is for getting ip address of user
            data.save()

            # Generate order number 
            year = int(datetime.date.today().strftime('%y'))
            month = int(datetime.date.today().strftime('%m'))
            date = int(datetime.date.today().strftime('%d'))
            d = datetime.date(year,month,date) # it will stored time in this format
            current_date = d.strftime("%Y%M%D")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered = False, order_number = order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render (request, 'payments.html', context)
    else:
        return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id = order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id =transID)

        context = {
            'order': order,
            'ordered_products': ordered_products, 
            'order_number': order.order_number,
            'transID': Payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'order_complete.html', context)
    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('Home')

