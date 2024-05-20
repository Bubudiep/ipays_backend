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
from oauth2_provider.models import *
import base64
import logging
logger = logging.getLogger(__name__)

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

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = "__all__"
 
class UserServicesSerializer(serializers.ModelSerializer):
    AvatarIMG = serializers.CharField(source="Avatar.img", read_only=True)
    ServiceCode = serializers.CharField(source="ServiceCode.ServiceCode")
    class Meta:
        model = UserServices
        fields = "__all__"

    def create(self, validated_data):
        try:
            if validated_data.get('ServiceCode', None) is not None:
                try:
                    qs_ServiceCode = Services.objects.get(ServiceCode=validated_data['ServiceCode']['ServiceCode'])
                    validated_data['ServiceCode'] = qs_ServiceCode
                except Exception as e:
                    raise TypeError(f"Loại hình kinh doanh {validated_data['ServiceCode']['ServiceCode']} chưa được thêm vào!")
            
            obj = UserServices.objects.create(**validated_data)
            obj.save()
            return obj
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            lineno = exc_tb.tb_lineno
            file_path = exc_tb.tb_frame.f_code.co_filename
            file_name = os.path.basename(file_path)
            message = f"[{file_name}_{lineno}] {str(e)}"
            logger.debug(message)
            raise TypeError(message)
    
    def update(self, qs_data, validated_data):
        try:
            if validated_data.get('ServiceCode', None) is not None:
                qs_ServiceCode = Services.objects.get(ServiceCode=validated_data['Services']['ServiceCode'])
                validated_data['ServiceCode'] = qs_ServiceCode
            
            return super().update(qs_data, validated_data)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            lineno = exc_tb.tb_lineno
            file_path = exc_tb.tb_frame.f_code.co_filename
            file_name = os.path.basename(file_path)
            message = f"[{file_name}_{lineno}] {str(e)}"
            logger.debug(message)
            raise TypeError(message)
        
 
class US_MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = US_Member
        fields = "__all__"
 
class US_FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = US_Floor
        fields = "__all__"
 
class US_RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = US_Rooms
        fields = "__all__"
class US_DeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = US_Desk
        fields = "__all__"
class US_MenuItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = US_MenuItems
        fields = "__all__"
class US_MenuSerializer(serializers.ModelSerializer):
    Items_list = US_MenuItemsSerializer(many=True, read_only=True)
    class Meta:
        model = US_Menu
        fields = "__all__"
class US_MenuTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = US_MenuType
        fields = "__all__"
class US_OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = US_Orders
        fields = "__all__"
class US_OrdersDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = US_OrdersDetails
        fields = "__all__"
class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = "__all__"
class US_HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = US_History
        fields = "__all__"
class IpaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ipays
        fields = "__all__"