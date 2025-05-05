from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home_view, name='home'),  # Home page
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),
    path('dashboard/milk_production/', views.milk_production, name='milk_production'),
    path('dashboard/shops/', views.shops, name='shops'),
    path('add-shop/', views.add_nandini_shop, name='add_nandini_shop'),
    path('dashboard/vehicles/', views.vehicles, name='vehicles'),
    path('dashboard/orders/', views.orders, name='order_list'),
    path('dashboard/quality_control/', views.quality_control, name='quality_control'),
    path('dashboard/milk_variants/', views.milk_variants, name='milk_variants'),
    path('dashboard/pricing_strategies/', views.pricing_strategies, name='pricing_strategies'),
    path('dashboard/orders/', views.orders, name='order_list'),
    path('home/', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forget-password/', views.forget_password_view, name='forget_password'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('orders/add/', views.add_order, name='add_order')
    
    
]
