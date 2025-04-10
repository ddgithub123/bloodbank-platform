from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import DonorProfile, DonationRecord  # Assuming you have a DonationRecord model
from django.contrib.auth.models import User  # Import User model if needed
# Create your views here.

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            print(f"🔍 DEBUG: Trying to authenticate with email: {email}, password: {password}")  # Debugging

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                print(f"User {user.email} authenticated successfully.")  # Debugging

                # Redirect based on role
                if hasattr(user, 'role'):  # Ensure role exists
                    if user.role == 'admin':
                        return redirect('adminpage')
                    elif user.role == 'donor':
                        return redirect('donor')
                    elif user.role == 'organization':
                        return redirect('organization')
                    else:
                        msg = 'Invalid role'
                        print("Invalid role assigned to user.")  # Debugging
                else:
                    msg = 'User role is missing'
                    print("User role field is missing.")  # Debugging
            else:
                msg = 'Invalid credentials'
                print("Authentication failed!")  # Debugging
        else:
            msg = 'Error validating form'
            print("Form validation failed.")  # Debugging

    return render(request, 'login.html', {'form': form, 'msg': msg})
def index(request):
    return render(request, 'index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})


def admin(request):
    return render(request,'admin.html')

@login_required
def donor_dashboard(request):
    try:
        donor = DonorProfile.objects.get(user=request.user)
        last_donation = DonationRecord.objects.filter(donor=donor).order_by('-donation_date').first()
    except DonorProfile.DoesNotExist:
        donor = None
        last_donation = None

    context = {
        'user': request.user,
        'last_donation_date': last_donation.donation_date if last_donation else "No donations yet",
        'last_donation_location': last_donation.organization.address if last_donation else "N/A",
        'verified': donor.verified if donor else False,
    }
    return render(request, 'donor_dash.html', context)


def recipient(request):
    return render(request,'recipient_dash.html')

def organization(request):
    return render(request,'org_dash.html')
from django.shortcuts import render

from .models import DonorProfile, VerificationRequest
from .forms import DonorProfileForm
from django.utils import timezone

@login_required
def donor_profile(request):
    donor, _ = DonorProfile.objects.get_or_create(user=request.user)
    form = DonorProfileForm(request.POST or None, instance=donor)
    msg = ""

    if request.method == 'POST' and form.is_valid() and 'apply_verification' not in request.POST:
        form.save()
        msg = "Profile updated successfully."

    can_apply = (
        not donor.verified and 
        not donor.applied_for_verification and 
        donor.blood_group and donor.disease_history
    )

    if request.method == 'POST' and 'apply_verification' in request.POST and can_apply:
        VerificationRequest.objects.create(
            donor=donor,
            organization=None,
            status='pending'
        )
        donor.applied_for_verification = True
        donor.save()
        msg = "Verification request sent."

    return render(request, 'donor/profile.html', {
        'form': form,
        'msg': msg,
        'can_apply': can_apply,
        'verified': donor.verified,
        'donor': donor,  # ✅ Add this for displaying profile values
    })



'''---------------------------------------------------------------------------------------------------------------------------'''
from .models import DonationRecord, DonorProfile

@login_required
def donor_my_donations(request):
    try:
        donor = DonorProfile.objects.get(user=request.user)
        donations = DonationRecord.objects.filter(donor=donor).order_by('-donation_date')
    except DonorProfile.DoesNotExist:
        donations = []

    return render(request, 'donor/my_donations.html', {'donations': donations})
'''-----------------------------------------------------------------------------------------------------------------------------'''



@login_required
def donor_book_appointment(request):
    donor = DonorProfile.objects.get(user=request.user)
    if not donor.verified:
        return render(request, 'donor/not_verified.html')  # Show a message page

    # else proceed to appointment booking


def donor_nearby_camps(request):
    """ View for finding nearby blood donation camps """
    return render(request, 'donor/nearby_camps.html')


def donor_contact_support(request):
    """ View for finding nearby blood donation camps """
    return render(request, 'donor/contact_support.html')
