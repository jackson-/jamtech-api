from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from . import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from . import models
from . import serializers


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000    

class UserListView(generics.ListCreateAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    pagination_class = StandardResultsSetPagination
    authentication_classes = (TokenAuthentication,)

class UserDetailView(generics.RetrieveAPIView):
    
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
    queryset = models.BusinessProfile.objects.select_related('user').all()
    serializer_class = serializers.ProfileSerializer
    pagination_class = StandardResultsSetPagination
    filterset_fields = [f.name for f in models.BusinessProfile._meta.fields]
    authentication_classes = (TokenAuthentication,)

class ProfileDetailView(generics.RetrieveAPIView):
    lookup_field = "id"
    queryset = models.BusinessProfile.objects.select_related('user').all()
    serializer_class = serializers.ProfileSerializer
    authentication_classes = (TokenAuthentication,)