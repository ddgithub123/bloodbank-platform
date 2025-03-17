from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_admin= models.BooleanField('Is admin', default=False)
    is_donor = models.BooleanField('Is donor', default=False)
    is_recipient = models.BooleanField('Is recipient', default=False)
    is_organization = models.BooleanField('Is organization', default=False)

