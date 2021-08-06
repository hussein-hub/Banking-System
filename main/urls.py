from django.contrib import admin
from django.urls import path, include
# importing views
from bankingApp import settings
from django.contrib.staticfiles.urls import static
from . import views
from main.views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('customers/', views.customers, name='customers'),
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('transfer/', views.transfer, name='transfer'),
    path('transaction/', views.transaction, name='transaction'),
    path('register/', views.register_user, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL)