from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('', views.UserListView.as_view()),
    re_path('(?P<id>[0-9]+)/$', views.UserDetailView.as_view()),
]