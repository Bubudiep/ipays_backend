import os, sys
import ast
import pytz
import requests
from django.utils import timezone
from dataclasses import fields
from re import I
import datetime
from tkinter import Label
from datetime import datetime as dt
import datetime as dto
from rest_framework import serializers
from zoneinfo import ZoneInfo
from .models import *
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from datetime import datetime, timedelta

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
        extra_kwargs = {
            'password': {'write_only': True}
        }

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255)

class PhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = "__all__"
 
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
 