from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),
    path('donor/', views.donor_dashboard, name='donor'),
    path('recipient/', views.recipient, name='recipient'),
    path('organization/', views.organization, name='organization'),

    #donor page urls
    path('donor/profile/', views.donor_profile, name='donor_profile'),
    path('donor/my-donations/', views.donor_my_donations, name='donor_my_donations'),
    path('donor/book-appointment/', views.donor_book_appointment, name='donor_book_appointment'),
    path('donor/nearby-camps/', views.donor_nearby_camps, name='donor_nearby_camps'),
    path('donor/contact-support/', views.donor_contact_support, name='contact_support'),

]

