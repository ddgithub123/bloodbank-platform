from django import forms
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
#from django.contrib.auth.forms import UserCreationForm



class User(AbstractUser):  # Custom User Model
    email = models.EmailField(unique=True)  # ✅ Ensure email is unique
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('donor', 'Donor'),
        ('organization', 'Organization'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='donor')

    USERNAME_FIELD = 'email'  # ✅ This makes email the unique identifier
    REQUIRED_FIELDS = ['username']  # Keeps username optional

class DonorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    disease_history = models.TextField(blank=True, null=True)
    verified = models.BooleanField(default=False)  # ✅ Verification Status
    last_donation_date = models.DateField(null=True, blank=True)
    total_donations = models.PositiveIntegerField(default=0)  # ✅ Track Donations
    applied_for_verification = models.BooleanField(default=False)  # ✅ Prevent multiple requests


    def apply_for_verification(self):
        """ Marks donor as applied for verification """
        if not self.verified:
            self.applied_for_verification = True
            self.save()


# Organization Profile
class OrganizationProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    verified = models.BooleanField(default=False)

#from django.contrib.gis.db import models as gis_models

class BloodCamp(models.Model):
    organization = models.ForeignKey(OrganizationProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = 23 #gis_models.PointField()  # ✅ Store as a geographical point
    start_date = models.DateField()
    end_date = models.DateField()
    contact_info = models.CharField(max_length=50)

    @staticmethod
    def get_nearby_camps(user_location, max_distance=50):
        return BloodCamp.objects.filter(
            location__distance_lte=(user_location, max_distance)
        )

# Appointment Booking
from datetime import timedelta, date

class Appointment(models.Model):
    donor = models.ForeignKey(DonorProfile, on_delete=models.CASCADE)
    camp = models.ForeignKey(BloodCamp, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('missed', 'Missed')
    ])

    def save(self, *args, **kwargs):
        # Ensure a donor does not book within 30 days
        last_appointment = Appointment.objects.filter(
            donor=self.donor, status="completed"
        ).order_by('-appointment_date').first()

        if last_appointment:
            min_next_date = last_appointment.appointment_date + timedelta(days=30)
            if self.appointment_date < min_next_date:
                raise ValueError("You cannot book another appointment within 30 days!")

        super().save(*args, **kwargs)


# Blood Inventory
class BloodInventory(models.Model):
    organization = models.ForeignKey(OrganizationProfile, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5)
    quantity = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

class DonationRecord(models.Model):
    donor = models.ForeignKey(DonorProfile, on_delete=models.CASCADE)
    organization = models.ForeignKey(OrganizationProfile, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5)
    amount = models.FloatField()
    donation_date = models.DateField(auto_now_add=True)
    expires_on = models.DateField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Update donor's total donations count
        self.donor.total_donations += 1
        self.donor.last_donation_date = self.donation_date
        self.donor.save()

        # ✅ Track Monthly Streaks
        streak, created = DonationStreak.objects.get_or_create(
            donor=self.donor,
            month=self.donation_date.month,
            year=self.donation_date.year,
        )
        streak.donations_count += 1
        streak.save()


# Blood Requests (Recipient Requests)
class BloodRequest(models.Model):
    organization = models.ForeignKey(OrganizationProfile, on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=255)
    blood_group = models.CharField(max_length=5)
    amount_needed = models.FloatField()
    disease_history = models.TextField()
    status = models.CharField(
        max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def complete_request(self):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()

# Verification Requests
class VerificationRequest(models.Model):
    donor = models.ForeignKey(DonorProfile, on_delete=models.CASCADE)
    organization = models.ForeignKey(OrganizationProfile, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=[('pending', 'Pending'), ('verified', 'Verified'), ('rejected', 'Rejected')]
    )
    verification_date = models.DateField(null=True, blank=True)

# Donation Streaks
class DonationStreak(models.Model):
    donor = models.ForeignKey(DonorProfile, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    donations_count = models.IntegerField(default=0)
