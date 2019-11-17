from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import ugettext_lazy as _
from .models import CustomUser, BusinessProfile, SpecialCredential

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs): 
        super(CustomUserCreationForm, self).__init__(*args, **kwargs) 
        self.fields['employer'] = forms.BooleanField(label=_("Employer?"), initial=True, required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'employer', 'profile')
        

class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs): 
        super(CustomUserChangeForm, self).__init__(*args, **kwargs) 
        self.fields['employer'] = forms.BooleanField(label=_("Employer?"), initial=True, required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'employer', 'profile')


class BusinessProfileCreationForm(forms.ModelForm):

    class Meta:
        model = BusinessProfile
        fields = ('company_name', 'industry_category', 'industry_segment',
     'experience_level', 'summary', 'zipcode', 'recent_projects', 'work_seeking')

class BusinessProfileChangeForm(forms.ModelForm):

    class Meta:
        model = BusinessProfile
        fields =  fields = ('company_name', 'industry_category', 'industry_segment',
     'experience_level', 'summary', 'zipcode', 'recent_projects', 'work_seeking')


class SpecialCredentialCreationForm(forms.ModelForm):

    class Meta:
        model = SpecialCredential
        fields = ('name', 'website', 'business')

class SpecialCredentialChangeForm(forms.ModelForm):

    class Meta:
        model = SpecialCredential
        fields =  fields = ('name', 'website', 'business')