from django.urls import path
from . import views

# write your urls 
urlpatterns = [
    # path('signup/',views.fxnsignup, name='signup'),
    path('',views.fxnsignup, name='signup'),
    path('signin/',views.fxnsignin, name='signin'),
    path('signout/',views.fxnsignout, name='signout'),
    path('dashboard/',views.fxndashboard, name='dashboard'),

    path('activate/<uidb64>/<token>/',views.fxnactivate, name='activate'),
    path('forgotPassword/', views.fxnforgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/',views.fxnValidateResetPassword, name='resetpassword_validate'),
    path('resetPassword/', views.fxnResetPassword, name='resetPassword'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('change_password/', views.change_password, name='change_password'),

    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),



]