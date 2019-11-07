from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from . import models
from rest_framework.authentication import authenticate



class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    from rest_auth.registration.serializers import RegisterSerializer


class CustomRegisterSerializer(RegisterSerializer):

    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    name = serializers.CharField(required=False)
    employer = serializers.BooleanField(required=True)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'password': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'name': self.validated_data.get('name', ''),
            'employer': self.validated_data.get('employer', ''),
        }
        

    def save(self, *args, **kwargs):
        cleaned_data = self.get_cleaned_data()
        user = models.CustomUser.objects.create(**cleaned_data)
        user.set_password(cleaned_data['password'])
        user.save()
        return user

class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomUser
        fields = ('email','name','employer', 'profile')
        read_only_fields = ('email')


class ProfileSerializer(serializers.ModelSerializer):

    def get_cleaned_data(self):
        return {
            'company_name': self.validated_data.get('company_name', ''),
            'industry_category': self.validated_data.get('industry_category', ''),
            'industry_segment': self.validated_data.get('industry_segment', ''),
            'experience_level': self.validated_data.get('experience_level', ''),
            'recent_project': self.validated_data.get('recent_project', ''),
            'work_seeking': self.validated_data.get('work_seeking', ''),
            'summary': self.validated_data.get('summary', ''),
            'zipcode': self.validated_data.get('zipcode', ''),
        }
        

    def save(self, *args, **kwargs):
        cleaned_data = self.get_cleaned_data()
        return models.BusinessProfile.objects.create(**cleaned_data)

    class Meta:
        model = models.BusinessProfile
        fields = ('id','company_name', 'industry_category', 'industry_segment', 'experience_level',
            'recent_project', 'work_seeking', 'summary', 'zipcode')

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = models.CustomUser
        fields = ('id', 'email', 'name', 'is_staff', 'employer', 'profile')
