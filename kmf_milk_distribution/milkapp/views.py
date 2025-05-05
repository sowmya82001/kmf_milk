from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import SignUpForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
from django.contrib.auth.models import User
from .models import OTPStorage
from django.core.mail import send_mail
import random
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .models import MilkProduction, NandiniShop, Vehicle, DeliverySchedule, Order, QualityControl, MilkVariant, PricingStrategy
from django.http import HttpResponse

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)  # Use the new form with CAPTCHA
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials or CAPTCHA, please try again.")
    else:
        form = LoginForm()  # Use the new form with CAPTCHA

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def forget_password_view(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                otp = str(random.randint(100000, 999999))
                OTPStorage.objects.update_or_create(user=user, defaults={'otp': otp})
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp}',
                    'admin@example.com',
                    [email],
                    fail_silently=False,
                )
                request.session['reset_email'] = email
                return redirect('reset_password')
            except User.DoesNotExist:
                form.add_error('email', 'Email not found.')
    else:
        form = ForgetPasswordForm()
    return render(request, 'forget_password.html', {'form': form})

def reset_password_view(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            new_password = form.cleaned_data['new_password']
            email = request.session.get('reset_email')
            if email:
                try:
                    user = User.objects.get(email=email)
                    otp_obj = OTPStorage.objects.get(user=user)
                    if otp_obj.otp == otp:
                        user.set_password(new_password)
                        user.save()
                        otp_obj.delete()
                        return redirect('login')
                    else:
                        form.add_error('otp', 'Invalid OTP')
                except (User.DoesNotExist, OTPStorage.DoesNotExist):
                    form.add_error('otp', 'Invalid attempt')
            else:
                form.add_error(None, 'Session expired, try again')
    else:
        form = ResetPasswordForm()
    return render(request, 'reset_password.html', {'form': form})

def home_view(request):
    return render(request, 'milkapp/home.html')

def logout_user(request):
    logout(request)
    return redirect('/')
# Milk Production & Procurement Data
def milk_production(request):
    productions = MilkProduction.objects.all()
    return render(request, 'dashboard/milk_production.html', {'productions': productions})

# Shop Registration & Demand Forecasting
def shops(request):
    shops = NandiniShop.objects.all()
    return render(request, 'dashboard/shops.html', {'shops': shops})

def add_nandini_shop(request):
    if request.method == 'POST':
        shop_name = request.POST['shop_name']
        location = request.POST['location']
        owner_name = request.POST['owner_name']
        contact_number = request.POST['contact_number']
        email = request.POST['email']
        weekly_demand_liters = request.POST['weekly_demand_liters']
        NandiniShop.objects.create(shop_name=shop_name, location=location, owner_name=owner_name,
                                    contact_number=contact_number, email=email,
                                    weekly_demand_liters=weekly_demand_liters)
        return redirect('nandini_shop_list')
    return render(request, 'add_nandini_shop.html')

# Logistics & Distribution Network
def vehicles(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'dashboard/vehicles.html', {'vehicles': vehicles})

def delivery_schedule_list(request):
    schedules = DeliverySchedule.objects.all()
    return render(request, 'delivery_schedule_list.html', {'schedules': schedules})

# Order Management System
def orders(request):
    orders = Order.objects.all()
    return render(request, 'dashboard/orders.html', {'orders': orders})

def add_order(request):
    if request.method == 'POST':
        shop = NandiniShop.objects.get(id=request.POST['shop_id'])
        milk_quantity_liters = request.POST['milk_quantity_liters']
        order_date = request.POST['order_date']
        delivery_date = request.POST['delivery_date']
        status = request.POST['status']
        Order.objects.create(shop=shop, milk_quantity_liters=milk_quantity_liters,
                             order_date=order_date, delivery_date=delivery_date, status=status)
        return redirect('order_list')
    shops = NandiniShop.objects.all()
    return render(request, 'add_order.html', {'shops': shops})

# Quality Control & Storage Facilities
def quality_control(request):
    quality_checks = QualityControl.objects.all()
    return render(request, 'dashboard/quality_control.html', {'quality_checks': quality_checks})

# Financial & Pricing Data
def milk_variants(request):
    variants = MilkVariant.objects.all()
    return render(request, 'dashboard/milk_variants.html', {'variants': variants})

def pricing_strategies(request):
    pricing_strategies = PricingStrategy.objects.all()
    return render(request, 'dashboard/pricing_strategies.html', {'pricing_strategies': pricing_strategies})

def add_pricing_strategy(request):
    if request.method == 'POST':
        variant = MilkVariant.objects.get(id=request.POST['variant_id'])
        region = request.POST['region']
        subsidy = request.POST['subsidy']
        PricingStrategy.objects.create(variant=variant, region=region, subsidy=subsidy)
        return redirect('pricing_strategy_list')
    variants = MilkVariant.objects.all()
    return render(request, 'add_pricing_strategy.html', {'variants': variants})

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')  # Dashboard template

def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'invoice.html', {'order': order})