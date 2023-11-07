from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    status = models.TextField(max_length=100, blank=True, null=True, verbose_name="Status")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, verbose_name="Gender")

