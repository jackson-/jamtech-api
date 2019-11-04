from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import (
    CustomUserCreationForm, CustomUserChangeForm,
    BusinessProfileChangeForm, BusinessProfileCreationForm,
    SpecialCredentialCreationForm, SpecialCredentialChangeForm
)
from .models import CustomUser, BusinessProfile, SpecialCredential

class CustomUserAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(CustomUserAdmin, self).__init__(*args, **kwargs) 

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'name', 'is_staff', 'employer']
    # exclude = ('last_name', 'date_joined', 'first_name')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2','employer')
        }),
    )
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name','employer')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)

class BusinessProfileAdmin(admin.ModelAdmin):
    add_form = BusinessProfileCreationForm
    form = BusinessProfileChangeForm
    model = BusinessProfile
    list_display = ['company_name', 'industry_category', 'industry_segment',
     'experience_level', 'summary', 'user']

admin.site.register(BusinessProfile, BusinessProfileAdmin)

class SpecialCredentialAdmin(admin.ModelAdmin):
    add_form = SpecialCredentialCreationForm
    form = SpecialCredentialChangeForm
    model = SpecialCredential
    list_display = ['name', 'website', 'business']

admin.site.register(SpecialCredential, SpecialCredentialAdmin)