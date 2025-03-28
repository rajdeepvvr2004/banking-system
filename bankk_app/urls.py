from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('transaction_history/', views.transaction_history_view, name='transaction_history'),
    path('otp_verify<str:operation>/',views.otp_verify,name="otp_verify"),
    path('reset_password_request/',views.reset_password_request,name="reset_password_request"),
    path('reset_password/',views.reset_password,name="reset_pass"),
    path('register2',views.register2,name="register2")
]