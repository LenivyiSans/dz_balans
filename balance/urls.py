from django.urls import path
from . import views

urlpatterns = [
    path('', views.account_list, name='account_list'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/create/', views.transaction_create, name='transaction_create'),
    path('transactions/<int:pk>/annul/', views.transaction_annul, name='transaction_annul'),
]
