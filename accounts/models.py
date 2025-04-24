from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    bio = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    birth_date = models.DateField(null=False, blank=False, default="2005-10-07")
    is_verified = models.BooleanField(default=False)
    location = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.username
    