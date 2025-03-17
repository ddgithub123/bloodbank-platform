from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),
    path('donor/', views.donor, name='donor'),
    path('recipient/', views.recipient, name='recipient'),
    path('organization/', views.organization, name='organization'),
]