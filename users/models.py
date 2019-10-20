from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    name = models.CharField(blank=True, max_length=255)
    employer = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class BusinessProfile(models.Model):
    company_name = models.CharField(blank=True, max_length=255)
    industry_category = models.CharField(blank=True, max_length=255)
    industry_segment = models.CharField(blank=True, max_length=255)
    experience_level = models.CharField(blank=True, max_length=255)
    recent_project = models.CharField(blank=True, max_length=255)
    work_seeking = models.CharField(blank=True, max_length=255)
    summary = models.CharField(blank=True, max_length=255)
    zipcode = models.CharField(blank=True, max_length=10)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.company_name

class SpecialCredential(models.Model):
    name = models.CharField(blank=True, max_length=255)
    website = models.CharField(blank=True, max_length=255)
    business = models.ForeignKey(
        BusinessProfile,
        on_delete=models.CASCADE,
    )