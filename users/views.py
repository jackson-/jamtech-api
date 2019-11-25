from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser, FormParser
from rest_framework.pagination import PageNumberPagination, InvalidPage
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import UpdateModelMixin
from . import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from django.forms.models import model_to_dict

from . import models
from . import serializers


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })


class UserListView(generics.ListCreateAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    pagination_class = StandardResultsSetPagination
    authentication_classes = (TokenAuthentication,)

class UserDetailView(generics.RetrieveAPIView, generics.UpdateAPIView):
    
    lookup_field = "id"
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, id=None):
        """
        If provided 'pk' is "me" then return the current user.
        """
        if request.user and id == 'me':
            return Response(serializers.UserSerializer(request.user).data)
        return super(UserDetailView, self).retrieve(request, id)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if(request.data['profile']):
            profile = models.BusinessProfile.objects.get(id=request.data['profile'])
            instance.profile = profile
            instance.save()
        models.CustomUser.objects.filter(id=kwargs['id']).update(**request.data)
        user = models.CustomUser.objects.select_related('profile').get(id=kwargs['id'])
        return Response(serializers.UserSerializer(user).data)






class ChangePasswordView(generics.UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = serializers.ChangePasswordSerializer
        model = models.CustomUser
        permission_classes = (IsAuthenticated,)
        authentication_classes = (TokenAuthentication,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                return Response("Success.", status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileListView(generics.ListCreateAPIView):
    queryset = models.BusinessProfile.objects.all()
    serializer_class = serializers.ProfileSerializer
    pagination_class = StandardResultsSetPagination
    filterset_fields = [f.name for f in models.BusinessProfile._meta.fields]
    authentication_classes = (TokenAuthentication,)
    filter_backends = [filters.SearchFilter]
    search_fields = [f.name for f in models.BusinessProfile._meta.fields]

    def create(self, request):
        response = super(ProfileListView, self).create(request)
        profile = models.BusinessProfile.objects.get(id=response.data['id'])
        if(request.data.get('credentials')):
            creds = request.data.get('credentials')
            for c in creds:
                c['business'] = profile
                models.SpecialCredential.objects.create(**c)
        return Response(serializers.ProfileSerializer(profile).data)

class ProfileDetailView(generics.RetrieveAPIView, generics.UpdateAPIView):
    lookup_field = "id"
    queryset = models.BusinessProfile.objects.all()
    serializer_class = serializers.ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    parser_classes = (MultiPartParser, JSONParser, FormParser, FileUploadParser)

    def update(self, request, *args, **kwargs):
        response = super(ProfileDetailView , self).update(request, args, kwargs)
        profile = models.BusinessProfile.objects.get(id=response.data['id'])
        profile.credentials.all().delete()
        if(request.data.get('credentials')):
            creds = request.data.get('credentials')
            new_creds = []
            for cred in creds:
                    cred['business'] = profile
                    new_creds.append(models.SpecialCredential.objects.create(**cred))
            profile.credentials.set(new_creds)
        return Response(serializers.ProfileSerializer(profile).data)
