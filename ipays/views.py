from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework import status
from django.conf import settings
from .models import Room
from rest_framework import viewsets, generics
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from .serializers import * 
from rest_framework import permissions
from rest_framework.decorators import action
import numpy as np
from oauth2_provider.models import *
import logging
logger = logging.getLogger(__name__)


def to_json(result:str, message:str, data:dict={}):
    return {"result": result, "message": message, "data": data}

def unique(list1):
    x = np.array(list1)
    return np.unique(x)

def check_token(a):
    if a.request.user.is_anonymous:
        token = a.request.headers.get('Authorization')
        if token is None:
            return None
        else:
            user=AccessToken.objects.get(token=token).user
            return user
    else:
        return a.request.user

def diff2list(l1: list, l2: list):
    li1 = np.array(l1)
    li2 = np.array(l2)
    
    dif1 = np.setdiff1d(li1, li2)
    dif2 = np.setdiff1d(li2, li1)
    
    return np.concatenate((dif1, dif2))

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
 
class StandardPagesPagination(PageNumberPagination):  
    page_size = 500

class AuthInfo(APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=HTTP_200_OK)
    
def index_view(request):
    return render(request, 'index.html', {
        'rooms': Room.objects.all(),
    })

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def room_view(request, room_name):
    chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(request, 'room.html', {
        'room': chat_room,
    })

class UserViewsets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardPagesPagination
    
    def get_permissions(self):
        if self.action == 'set_password':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
        # return [permissions.IsAuthenticated()]
                
    @action(methods=['post'], detail=True, url_path='set-password', url_name='set-password')
    # detail=True: have pk parameter
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    # detail=False : don't have pk parameter
    def recent_users(self, request):
        recent_users = User.objects.all().order_by('-last_login')
        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)

    def list(self, request):
        qs_data = self.get_queryset()
        ip_client = get_client_ip(request)
        user=check_token(self)
        logger.debug(user)
        if user is None:
            return Response("No authorization", status=HTTP_400_BAD_REQUEST)
        
        if user.username != "admin":
            qs_data=qs_data.filter(username=user.username)
        page = self.paginate_queryset(qs_data)
        if page is not None:
            # logger.debug(page)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(qs_data, many=True)
        return Response(serializer.data)
 