# chat/urls.py
from django.urls import path, include
from . import views
from django.contrib.auth.models import User
from rest_framework import routers

router = routers.DefaultRouter()
router.register("users", views.UserViewsets, basename="users")
router.register("Photos", views.PhotosViewsets, basename="Photos")
router.register("UserProfile", views.UserProfileViewsets, basename="UserProfile")
urlpatterns = [
    path('oauth2-info/', views.AuthInfo.as_view()),
    path('', include(router.urls)),
]