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


def generate_response_json(result:str, message:str, data:dict={}):
    """_summary_

    Args:
        result (str): PASS / FAIL
        message (str): Description
        data (dict): dict data

    Raises:
        Exception: _description_

    Returns:
        dict: Response Packaged
    """
    # logger.debug(f"Result: {result}, Message: {message}, Data: {data}")
    return {"result": result, "message": message, "data": data}

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
            
class PhotosViewsets(viewsets.ModelViewSet):
    queryset = Photos.objects.all()
    serializer_class = PhotosSerializer
    pagination_class = StandardPagesPagination
    permission_classes_by_action = {
        'get': [permissions.AllowAny()],
        'retrieve': [permissions.AllowAny()],
        'create': [permissions.AllowAny()],
        'list': [permissions.AllowAny()],
        'update': [permissions.AllowAny()],
        'partial_update': [permissions.AllowAny()],
    }
    
    def get_permissions(self):
        default_permissions = [permissions.IsAuthenticated()]
        return self.permission_classes_by_action.get(self.action, default_permissions)
    
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return Response({"message": {f"{e}"}}, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            lineno = exc_tb.tb_lineno
            file_path = exc_tb.tb_frame.f_code.co_filename
            file_name = os.path.basename(file_path)
            message = f"[{file_name}_{lineno}] {str(e)}"
            logger.debug(message)
            res_data = generate_response_json("FAIL", message)
            return Response(res_data, status=HTTP_404_NOT_FOUND)
    
    def list(self, request):
        try:
            qs_data = self.get_queryset()
            ip_client = get_client_ip(request)
             
            page_size = self.request.query_params.get('page_size')
            if page_size is not None:
                self.pagination_class.page_size = int(page_size)
                     
            page = self.paginate_queryset(qs_data)
            if page is not None:
                # logger.debug(page)
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
                     
            serializer = self.get_serializer(qs_data, many=True)
            return Response(serializer.data)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            lineno = exc_tb.tb_lineno
            file_path = exc_tb.tb_frame.f_code.co_filename
            file_name = os.path.basename(file_path)
            message = f"[{file_name}_{lineno}] {str(e)}"
            # logger.debug(message)
            res_data = generate_response_json("FAIL", message)
            return Response(res_data, status=HTTP_404_NOT_FOUND)
                 
class UserProfileViewsets(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    pagination_class = StandardPagesPagination
    permission_classes_by_action = {
        'get': [permissions.AllowAny()],
        'retrieve': [permissions.AllowAny()],
        'create': [permissions.AllowAny()],
        'list': [permissions.AllowAny()],
        'update': [permissions.AllowAny()],
        'partial_update': [permissions.AllowAny()],
    }
    
    def get_permissions(self):
        default_permissions = [permissions.IsAuthenticated()]
        return self.permission_classes_by_action.get(self.action, default_permissions)
    
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return Response({"message": {f"{e}"}}, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            lineno = exc_tb.tb_lineno
            file_path = exc_tb.tb_frame.f_code.co_filename
            file_name = os.path.basename(file_path)
            message = f"[{file_name}_{lineno}] {str(e)}"
            logger.debug(message)
            res_data = generate_response_json("FAIL", message)
            return Response(res_data, status=HTTP_404_NOT_FOUND)
    
    def list(self, request):
        try:
            qs_data = self.get_queryset()
            ip_client = get_client_ip(request)
             
            page_size = self.request.query_params.get('page_size')
            if page_size is not None:
                self.pagination_class.page_size = int(page_size)
                     
            page = self.paginate_queryset(qs_data)
            if page is not None:
                # logger.debug(page)
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
                     
            serializer = self.get_serializer(qs_data, many=True)
            return Response(serializer.data)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            lineno = exc_tb.tb_lineno
            file_path = exc_tb.tb_frame.f_code.co_filename
            file_name = os.path.basename(file_path)
            message = f"[{file_name}_{lineno}] {str(e)}"
            # logger.debug(message)
            res_data = generate_response_json("FAIL", message)
            return Response(res_data, status=HTTP_404_NOT_FOUND)
     