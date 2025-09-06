from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, UserForm, UserProfileForm
from . models import Account, UserProfile
from django.contrib import messages, auth
from  django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# carts USER app models & views
from carts.models import Cart, CartItem
from carts.views import _cart_id
from orders.models import Order, OrderProduct

# Verification email
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Lib
import requests

# Create your views here.

def fxnsignup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            Email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = Email.split("@")[0]
            user = Account.objects.create_user(first_name = first_name, last_name = last_name, email = Email, username = username, password = password ) 
            user.phone_number = phone_number
            user.save() 

            # Create a user profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()

            # User Activation
            current_site = get_current_site(request)
            mail_subject = 'Please Activate Your Account'
            message = render_to_string('account_verification_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_mail = Email
            send_mail = EmailMessage(mail_subject, message, to=[to_mail])
            send_mail.send()
            
            # messages.success(request,'We have sent a verification message to your email') 
            # return redirect ('signup')
            return redirect('/account/signin/?command=verification&email='+ Email)
            # account/signin/?command=verification&email=xyz@gmail.com

    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'sign_up.html',context)

def fxnsignin(request):
    if request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    # getting product variations by cart id
                    product_variation = []
                    for item in cart_item: 
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # 
                    cart_item = CartItem.objects.filter(user = user)
                    ex_var_list=[]
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item =CartItem.objects.get(id= item_id)
                            item.quantity += 1
                            item.user =user
                            item.save()
                        else:
                            cart_item=CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            url = request.META.get('HTTP_REFERER')
            try:
                query= requests.utils.urlparse(url).query
                # next redirect -- before:logout :: after: login 
                params = dict(x.split('=') for x in query.split('&')) 
                # it just works like : it will wplit wher is =  and before = will be taken as 'key' and after = will be taken as 'value'
                if 'next' in params:
                    nextpage = params['next']
                    return redirect(nextpage)
            except:
                return redirect('Home')
                
        else:
            messages.error(request, 'Invalid Login Credentails Please Try Again')
            return redirect('signin')
    return render(request, 'sign_in.html')

@login_required(login_url = 'signin')
def fxnsignout(request):
    auth.logout(request)
    messages.success(request, 'You are Logged out')
    return redirect('signin')


def fxnactivate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'congratulations! Your Account is Activated.')
        return redirect ('signin')
    else:
        messages.error(request, 'Invalid Activation Link')
        return redirect('signup')

@login_required(login_url = 'signin')
def fxndashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    return render(request, 'dashboard.html', context)


def fxnforgotPassword(request):
    if request.method == 'POST':
        MAIL = request.POST['email']
        if Account.objects.filter(email=MAIL).exists():
            user= Account.objects.get(email__exact=MAIL)

            # User Activation
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('reset_password_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_mail = MAIL
            send_mail = EmailMessage(mail_subject, message, to=[to_mail])
            send_mail.send()

            messages.success(request, 'Your request for password reset message has been sent to your registered Email.')
            return redirect ('signin')
        else:
            messages.error(request, 'Account does not exists!')
            return redirect('forgotPassword')

    return render(request, 'forgotPassword.html')


def fxnValidateResetPassword(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid']=uid
        messages.info(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('signin')

def fxnResetPassword(request):
    if request.method == 'POST':
        create_password = request.POST['password']
        cnf_password = request.POST['confirm_password']

        if  create_password == cnf_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(create_password)
            user.save()
            messages.success(request, 'Password Reset Successful')
            return redirect('signin')
        else:
            messages.error(request, 'Password Mismatch')
            return redirect('resetPassword')
    else:
        return render(request, 'ResetPassword.html')

@login_required(login_url='signin')
def my_orders(request):
    orders =  Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'my_orders.html', context)

@login_required(login_url='signin')
def my_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Yout Profile has been updated.')
            return redirect('my_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form' : user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'my_profile.html', context)



# @login_required(login_url='login')
# def my_profile(request):
#     userprofile, created = UserProfile.objects.get_or_create(
#         user=request.user,
#         defaults={"profile_picture": "default/default-user.png"}
#     )
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=request.user)
#         profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'Your Profile has been updated.')
#             return redirect('my_profile')
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = UserProfileForm(instance=userprofile)

#     context = {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'userprofile': userprofile,
#     }
#     return render(request, 'my_profile.html', context)

@login_required(login_url='signin')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password) # we didn't use any package for pasdw encode or decode ... we use the django hasing so .. here we use the buil-in check passdw method ..for hashing the passdw
            if success:
                user.set_password(new_password) # bilt-in function to take new  pass and set as the new pass.
                user.save()
                # auth.logout(request) --> after set pass ... it will logout user.
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'change_password.html')


@login_required(login_url='signin')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'order_detail.html', context)