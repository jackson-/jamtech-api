from rest_framework import generics, status
from rest_framework.response import Response
from . import serializers
from rest_framework.permissions import IsAuthenticated   

from . import models
from . import serializers

class UserListView(generics.ListAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return models.CustomUser.objects.filter(**self.request.GET.dict())

class UserDetailView(generics.RetrieveAPIView):
    lookup_field = "id"
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer



class ChangePasswordView(generics.UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = serializers.ChangePasswordSerializer
        model = models.CustomUser
        permission_classes = (IsAuthenticated,)

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

    def get_queryset(self):
        breakpoint()
        return models.BusinessProfile.objects.select_related('user').filter(**self.request.GET.dict())

class ProfileDetailView(generics.RetrieveAPIView):
    lookup_field = "id"
    queryset = models.BusinessProfile.objects.select_related('user').all()
    serializer_class = serializers.ProfileSerializer()