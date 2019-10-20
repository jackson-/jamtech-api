from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, BusinessProfile, SpecialCredential

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'employer')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields =  fields = ('username', 'email', 'name', 'employer')


class BusinessProfileCreationForm(UserCreationForm):

    class Meta:
        model = BusinessProfile
        fields = ('company_name', 'industry_category', 'industry_segment',
     'experience_level', 'summary', 'user')

class BusinessProfileChangeForm(UserChangeForm):

    class Meta:
        model = BusinessProfile
        fields =  fields = ('company_name', 'industry_category', 'industry_segment',
     'experience_level', 'summary', 'user')


class SpecialCredentialCreationForm(UserCreationForm):

    class Meta:
        model = SpecialCredential
        fields = ('name', 'website', 'business')

class SpecialCredentialChangeForm(UserChangeForm):

    class Meta:
        model = SpecialCredential
        fields =  fields = ('name', 'website', 'business')