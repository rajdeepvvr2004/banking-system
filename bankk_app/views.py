# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import BankAccount, Transaction,SavingsAccount,FixedDepositAccount,CurrentAccount
from django.contrib.auth.decorators import login_required
import os
import smtplib
import random
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal



                

# Deposit View
def deposit_view(request):
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        username = request.session.get('logged_in_user')
        user = BankAccount.objects.get(username=username)

        otp = generate_otp()
        # user.otp = otp
        # user.save()
        send_otp_mail(user.email, otp)

        request.session['otp'] = otp
        request.session['pending_deposit_amount'] = str(amount)

        messages.success(request, "OTP sent to your email. Please verify.")
        return redirect('otp_verify',operation="deposit")
    
    return render(request, 'deposit.html')

# Withdraw View
def withdraw_view(request):
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        username = request.session.get('logged_in_user')
        user = BankAccount.objects.get(username=username)

        if amount > user.balance:
            messages.error(request, "Insufficient balance.")
            return redirect('withdraw')
        
        otp = generate_otp()
        # user.otp = otp
        # user.save()
        send_otp_mail(user.email, otp)

        request.session['otp'] = otp
        request.session['pending_withdraw_amount'] = str(amount)

        messages.success(request, "OTP sent to your email. Please verify.")
        return redirect('otp_verify', operation='withdraw')
    
    return render(request, 'withdraw.html')


def reset_password_request(request):
    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']

        user = None  # Initialize user as None

        if BankAccount.objects.filter(username=username_or_email).exists():
            user = BankAccount.objects.get(username=username_or_email)
        
        elif BankAccount.objects.filter(email=username_or_email).exists():
            user = BankAccount.objects.get(email=username_or_email)
        
        if user:
            # Generate OTP
            otp = generate_otp()

            # Send OTP to the user's registered email
            send_otp_mail(user.email, otp)

            # Store the username in session for verification later
            request.session['password_reset_user'] = user.username
            request.session['otp'] = otp


            messages.success(request, "An OTP has been sent to your registered email. Please check your inbox.")
            return redirect('otp_verify', operation='reset_password')
        
        messages.error(request, "No account found with that username or email.")

    return render(request, 'reset_password_request.html')

# Password Reset View
def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        username = request.session.get('password_reset_user')

        if not username:
            messages.error(request, "Something went wrong. Please try again.")
            return redirect('reset_password_request')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password')

        try:
            user = BankAccount.objects.get(username=username)
            user.password = new_password
            # user.otp = None  # Clear the OTP after successful reset
            user.save()
            
            # Clear session data
            del request.session['password_reset_user']

            messages.success(request, "Password has been successfully reset! You can now log in.")
            return redirect('login')
        except BankAccount.DoesNotExist:
            messages.error(request, "User not found. Please try again.")
    
    return render(request, 'reset_password.html')




# Generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Generate Unique Account Number
def generate_account_number():
    while True:
        account_number = str(random.randint(100000000000, 999999999999))
        if not BankAccount.objects.filter(accountno=account_number).exists():  # Updated field name
            return account_number

# Home Page
def home(request):
    return render(request, 'home.html')


# Login Function
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if BankAccount.objects.filter(username=username,password=password).exists():
              user = BankAccount.objects.get(username=username, password=password)
              request.session['logged_in_user'] = username  # Store the username in the session
              messages.success(request, "Login successful!")
              return redirect('dashboard')
        else:
             messages.error(request, "Invalid username or password.")
             return redirect('login')
        
    return render(request, 'login.html')    


# Logout Function
def logout_view(request):
    if 'logged_in_user' in request.session:
        del request.session['logged_in_user']
    messages.info(request, "You have been logged out.")
    return redirect('login')


def dashboard_view(request):
     username = request.session.get('logged_in_user')
     if not username:
        return redirect('login')
    
     user = BankAccount.objects.get(username=username)
    
    # Fetch the latest 5 transactions for the logged-in user
     transactions = Transaction.objects.filter(user=user).order_by('-date')[:5]
    
     return render(request, 'dashboard.html', {'user': user, 'transactions':transactions})

# View Transaction History
def transaction_history_view(request):
    username = request.session.get('logged_in_user')
    if not username:
        return redirect('login')
    
    user = BankAccount.objects.get(username=username)
    transactions = Transaction.objects.filter(user=user).order_by('-date')
    
    return render(request, 'history.html', {'transactions': transactions})

# Send OTP via Email
def send_otp_mail(email, otp):
    send_mail(
        'Your OTP Code',
        f'Your OTP is: {otp}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

# OTP Verification View
def otp_verify(request, operation):
    if request.method == 'POST':
        otp = request.POST['otp']
        original_otp = request.session.get('otp')

        if otp != original_otp:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("otp_verify",operation=operation)
          
        else:
            del request.session['otp']
            if operation == 'register':
                username = request.session.pop('username')
                password = request.session.pop('password')
                email = request.session.pop('email')
                accountno = request.session.pop('accountno')
                bal = request.session.pop("balance")
                accountype=request.session.get("accountype")

          
                if accountype=="savings":
                    user= BankAccount(
                        username=username,
                        password=password,
                        email=email,
                        accountno=accountno,
                        balance=bal
                        )
                    user.save()
                    SavingsAccount.objects.create(account=user,username=user.username)
                    messages.success(request, "Registration successful! You can now log in.")
                    return redirect('login')

                elif accountype=="current":
                            user=BankAccount(
                                username=username,
                                password=password,
                                email=email,
                                accountno=accountno,
                                balance=bal)
                            user.save()
                            CurrentAccount.objects.create(account=user,username=user.username) 
                            messages.success(request, "Registration successful! You can now log in.")
                            return redirect('login')

                elif accountype=="fd":
                    BankAccount.objects.create(
                                username=username,
                                password=password,
                                email=email,
                                accountno=accountno,
                                balance=bal
                                )
                    FixedDepositAccount.objects.create(account=user,username=user.username)   
                    messages.success(request, "Registration successful! You can now log in.")
                    return redirect('login')      

            elif operation == 'deposit':
                username = request.session.get('logged_in_user')
                user = BankAccount.objects.get(username=username)
                amount = Decimal(request.session.pop('pending_deposit_amount'))
                user.balance += amount
                user.save()
                Transaction.objects.create(user=user, type="Deposit", amount=amount)
                messages.success(request, f"Successfully deposited Rs {amount}.")
                return redirect('dashboard')

            elif operation == 'withdraw':
                username = request.session.get('logged_in_user')
                user = BankAccount.objects.get(username=username)
                amount = Decimal(request.session.pop('pending_withdraw_amount'))
                user.balance -= amount
                user.save()
                Transaction.objects.create(user=user, type="Withdraw", amount=amount)
                messages.success(request, f"Successfully withdrew Rs {amount}.")
                return redirect('dashboard')
   
    
    return render(request, 'otp_verify.html', {'operation': operation})

# Register View
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        # email = request.POST['email']
        accountype=request.POST["account_type"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if BankAccount.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')
        
 
        

        accountno = generate_account_number()  # Generate unique account number

        
        request.session['username'] = username
        request.session['password'] = password
       
        request.session['accountno'] = accountno
        request.session["accountype"]=accountype

        return redirect('register2')

    return render(request, 'register.html')

def register2(request):
    if request.method=="POST":
        balance = int(request.POST["balance"])
        accounttype=request.session.get("accountype")
        email=request.POST["email"]

        if BankAccount.objects.filter(email=email).exists():
            messages.error(request, "Try logging with a different email.")
            return redirect('register')


        if accounttype=="savings" and balance< 500:
            return redirect("register2")
        elif accounttype=="current" and balance<50000:
             return redirect("register2")
        elif accounttype=="fd" and balance<100000:
             return redirect("register2")
        else:
            otp = generate_otp()
            send_otp_mail(email, otp)
            request.session["balance"]=balance
            request.session['otp'] = otp
            request.session['email'] = email
            messages.success(request, "OTP sent to your email. Please verify.")
            return redirect('otp_verify',operation="register")
    return render(request,"registerdeposit.html")    

            
        



