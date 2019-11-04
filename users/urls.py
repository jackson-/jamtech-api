from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('password/reset/', views.ChangePasswordView.as_view()),
    re_path('profiles/(?P<id>[0-9]+)/$', views.ProfileDetailView.as_view()),
    path('profiles/', views.ProfileListView.as_view()),
    re_path('(?P<id>[0-9a-zA-Z]+)/$', views.UserDetailView.as_view()),
    path('', views.UserListView.as_view()),
]