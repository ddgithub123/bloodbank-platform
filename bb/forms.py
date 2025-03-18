from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# 🔹 Login Form (No phone number added)
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


# 🔹 Signup Form (User Registration)
class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    phone = forms.CharField(  # ✅ Added Phone Number only here
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2', 'is_admin', 'is_donor', 'is_recipient','is_organization')
