from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser, FormParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import UpdateModelMixin
from . import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from . import models
from . import serializers

import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'AKIAJSU5KNHPGBPSQEFA'
SECRET_KEY = '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'


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000    

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

class ProfileDetailView(generics.RetrieveAPIView, generics.UpdateAPIView):
    lookup_field = "id"
    queryset = models.BusinessProfile.objects.all()
    serializer_class = serializers.ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    parser_classes = (MultiPartParser, JSONParser, FormParser, FileUploadParser)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if('image' in request.FILES):
            img = request.FILES.get('image')
            session = boto3.Session(aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
            s3 = session.resource('s3')
            try:
                s3.Bucket('jamtech-images').put_object(Key='logos/%s' % img.name, Body=img)
                print("Upload Successful")
                instance.logo = "http://s3-us-east-1.amazonaws.com/jamtech-images/logos/{}".format(img.name)
                instance.save()
            except FileNotFoundError as e:
                print("The file was not found")
                return Response(e)
            except NoCredentialsError as e:
                print("Credentials not available")
                return Response(e)
            try:
                del request.data['image']
                models.BusinessProfile.objects.filter(id=kwargs['id']).update(**request.data)
                return Response(serializers.ProfileSerializer(instance).data)
            except Exception as e:
                print("Problem updating the Profile model")
                return Response(e)
        models.BusinessProfile.objects.filter(id=kwargs['id']).update(**request.data)
        instance.refresh_from_db()
        return Response(serializers.ProfileSerializer(instance).data)

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        profile = models.BusinessProfile.objects.get(id=self['pk']) 
        return Response(serializers.ProfileSerializer(profile).data)
