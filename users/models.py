from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.conf import settings

class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    use_in_migrations = True

    def create_user(self, email, name, employer, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        breakpoint()
        print("WE IUN HERE")
        user = self.model(
            email=self.normalize_email(email),
            employer=employer,
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(blank=True, max_length=255, null=True)
    name = models.CharField(blank=True, max_length=255)
    email = models.EmailField(unique=True)
    employer = models.BooleanField(blank=False, null=False)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active.'
            'Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'employer','name' ]

    objects = MyUserManager()

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