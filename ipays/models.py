# chat/models.py
from base64 import b64encode
from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
import logging
logger = logging.getLogger(__name__)

import datetime


class Room(models.Model):
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=User, blank=True)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'


class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user')
    to = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name='to', blank=True, null=True)
    room = models.ForeignKey(to=Room, on_delete=models.SET_NULL, blank=True, null=True)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'
    
class Photos(models.Model):
    file_name = models.CharField(max_length=100, default="", blank=True, null=True)
    file_type = models.CharField(max_length=100, default="", blank=True, null=True)
    file_size = models.IntegerField(blank=True, null=True)
    img= models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True)
    Comment = models.CharField(max_length=1024, default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def img_tag(self):
        try:
            return mark_safe('<img src = "{}" style="width:100px;border-radius: 10px;">'.format(
                self.img
            ))
        except Exception as e:
            logger.debug(e)
            return "aa"
    img_tag.short_description = 'Image'
    img_tag.allow_tags = True

    class Meta:
        ordering = ['-id']
    def __str__(self): 
        return f"{self.file_name}"
    
    
class UserProfile(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    fullname = models.CharField(max_length=100, default="", blank=True)
    birthday = models.DateField(null=True, blank=True)
    adr_tinh = models.CharField(max_length=100, default="", blank=True)
    adr_thanhpho = models.CharField(max_length=100, default="", blank=True)
    adr_huyen = models.CharField(max_length=100, default="", blank=True)
    adr_xa = models.CharField(max_length=100, default="", blank=True)
    comment = models.CharField(max_length=1024, default="", blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
    def __str__(self): 
        return f"{self.user.username}"
    
class Services(models.Model):
    ServiceCode = models.CharField(max_length=50,unique=True)
    ServiceName = models.CharField(max_length=225)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id']
    def __str__(self): 
        return f"{self.ServiceCode}"
  
class UserServices(models.Model):
    Status_CHOICES = (
        ["ACTIVE", "ACTIVE"],
        ["NOTACTIVE", "NOTACTIVE"],
    )
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    ServiceCode = models.ForeignKey(to=Services, on_delete=models.SET_NULL, null=True, blank=True)
    Status = models.CharField(max_length=100, default="ACTIVE", choices=Status_CHOICES, blank=True, null=True)
    
    Avatar = models.ForeignKey(to=Photos, on_delete=models.SET_NULL, null=True, blank=True)
    Name = models.CharField(max_length=225)
    Sologan = models.CharField(max_length=225, blank=True, null=True)
    Hotline = models.CharField(max_length=100, blank=True, null=True)
    Zalo = models.CharField(max_length=100, blank=True, null=True)
    Facebook = models.CharField(max_length=100, blank=True, null=True)
    IsPublic = models.BooleanField(default=True)

    adr_tinh = models.CharField(max_length=100, default="", blank=True)
    adr_huyen = models.CharField(max_length=100, default="", blank=True)
    adr_xa = models.CharField(max_length=100, default="", blank=True)
    adr_thon = models.CharField(max_length=100, default="", blank=True)
    adr_details = models.CharField(max_length=100, default="", blank=True)

    comment = models.CharField(max_length=1024, default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id']
    def __str__(self): 
        return f"{self.user} {self.ServiceCode.ServiceCode}"
    
class US_Member(models.Model):
    Type_CHOICES = (
        ["ADMIN", "ADMIN"],
        ["STAFF", "STAFF"],
    )
    UserServices = models.ForeignKey(to=UserServices, on_delete=models.CASCADE)
    Type = models.CharField(max_length=100, default="STAFF", choices=Type_CHOICES, blank=True, null=True)
    member = models.ForeignKey(to=User, on_delete=models.SET_NULL,related_name="member", null=True)
    user_add = models.ForeignKey(to=User, on_delete=models.SET_NULL,related_name="user_add", null=True)
    comment = models.CharField(max_length=1024, default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id']
    def __str__(self): 
        return f"{self.UserServices.Name} {self.Type}"    
    
class US_Floor(models.Model):
    Type_CHOICES = (
        ["ACTIVE", "ACTIVE"],
        ["NOTACTIVE", "NOTACTIVE"],
    )
    FloorName = models.CharField(max_length=100, default="", blank=True)
    UserServices = models.ForeignKey(to=UserServices, on_delete=models.CASCADE)
    Status = models.CharField(max_length=100, default="STAFF", choices=Type_CHOICES, blank=True, null=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    comment = models.CharField(max_length=1024, default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id']
    def __str__(self): 
        return f"{self.FloorName}"
       
class US_Rooms(models.Model):
    Type_CHOICES = (
        ["ACTIVE", "ACTIVE"],
        ["NOTACTIVE", "NOTACTIVE"],
    )
    RoomName = models.CharField(max_length=100, default="", blank=True)
    US_Floor = models.ForeignKey(to=US_Floor, on_delete=models.CASCADE)
    Status = models.CharField(max_length=100, default="STAFF", choices=Type_CHOICES, blank=True, null=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    comment = models.CharField(max_length=1024, default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id']
    def __str__(self): 
        return f"{self.RoomName}"
      
class US_Desk(models.Model):
    Type_CHOICES = (
        ["ACTIVE", "ACTIVE"],
        ["NOTACTIVE", "NOTACTIVE"],
    )
    DeskName = models.CharField(max_length=100, default="", blank=True)
    US_Rooms = models.ForeignKey(to=US_Rooms, on_delete=models.CASCADE)
    Status = models.CharField(max_length=100, default="STAFF", choices=Type_CHOICES, blank=True, null=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    comment = models.CharField(max_length=1024, default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id']
    def __str__(self): 
        return f"{self.RoomName}"
         
class US_Menu(models.Model):
    Type_CHOICES = (
        ["ACTIVE", "ACTIVE"],
        ["NOTACTIVE", "NOTACTIVE"],
    )
    UserServices = models.ForeignKey(to=UserServices, on_delete=models.CASCADE)
    MenuName = models.CharField(max_length=100, default="", blank=True)
    Status = models.CharField(max_length=100, default="ACTIVE", choices=Type_CHOICES, blank=True, null=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    comment = models.CharField(max_length=1024, default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id']
    def __str__(self): 
        return f"{self.MenuName}"
                  
class US_MenuType(models.Model):
    Type_CHOICES = (
        ["ACTIVE", "ACTIVE"],
        ["NOTACTIVE", "NOTACTIVE"],
    )
    US_Menu = models.ForeignKey(to=US_Menu, on_delete=models.CASCADE)
    TypeName = models.CharField(max_length=100, default="", blank=True)
    Status = models.CharField(max_length=100, default="ACTIVE", choices=Type_CHOICES, blank=True, null=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    comment = models.CharField(max_length=1024, default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id']
    def __str__(self): 
        return f"{self.TypeName}"
    
class US_MenuItems(models.Model):
    Type_CHOICES = (
        ["ACTIVE", "ACTIVE"],
        ["NOTACTIVE", "NOTACTIVE"],
    )
    US_MenuType = models.ForeignKey(to=US_MenuType, on_delete=models.CASCADE)
    Photos = models.ForeignKey(to=Photos, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100, default="", blank=True)
    Type = models.CharField(max_length=100, choices=Type_CHOICES, default="ACTIVE", blank=True)
    Price = models.IntegerField(default=0, null=True)
    Unit = models.CharField(max_length=100, blank=True, null=True)
    OrderOnline = models.BooleanField(default=True, null=True, blank=True)
    Discount = models.IntegerField(default=0, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    comment = models.CharField(max_length=1024, default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id']
    def __str__(self): 
        return f"{self.Name}"
    
class US_Orders(models.Model):
    UserServices = models.ForeignKey(to=UserServices, on_delete=models.CASCADE)
    US_Rooms = models.ForeignKey(to=US_Rooms, on_delete=models.SET_NULL, default="", blank=True, null=True)
    US_Desk = models.ForeignKey(to=US_Desk, on_delete=models.SET_NULL, default="", blank=True, null=True)
    OrderCode = models.CharField(max_length=100, default="", blank=True)
    staff = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name="staff")
    payVAT = models.IntegerField(default=0, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    isAccepted= models.BooleanField(default=False,null=True,blank=True)
    isShiped= models.BooleanField(default=False,null=True,blank=True)
    isCompleted= models.BooleanField(default=False,null=True,blank=True)
    comment = models.CharField(max_length=1024, default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id']
    def __str__(self): 
        return f"{self.OrderCode}"
    
class US_OrdersDetails(models.Model):
    US_Orders = models.ForeignKey(to=US_Orders, on_delete=models.SET_NULL, blank=True, null=True)
    US_MenuItems = models.ForeignKey(to=US_MenuItems, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    QTY = models.IntegerField(default=0, null=True)
    Price = models.IntegerField(default=0, null=True)
    comment = models.CharField(max_length=1024, default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id']
    def __str__(self): 
        return f"{self.US_Orders.OrderCode}"

class Voucher(models.Model):
    Type_CHOICES = (
        ["Percent", "Percent"],
        ["Price", "Price"],
    )
    VoucherCode = models.CharField(max_length=100, unique=True)
    UserServices = models.ForeignKey(to=UserServices, on_delete=models.SET_NULL, blank=True, null=True)
    US_MenuItems = models.ForeignKey(to=US_MenuItems, on_delete=models.SET_NULL, blank=True, null=True)
    Type = models.CharField(max_length=100, choices=Type_CHOICES, default="Percent", blank=True)
    Value = models.IntegerField(blank=True, null=True)
    MaxPrice = models.IntegerField(blank=True, null=True)
    LimitUses = models.IntegerField(blank=True, null=True)
    LimitHours = models.IntegerField(blank=True, null=True)
    isActive = models.BooleanField(default=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    comment = models.CharField(max_length=1024, default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id']
    def __str__(self): 
        return f"{self.VouncherCode}"

class US_History(models.Model):
    UserServices = models.ForeignKey(to=UserServices, on_delete=models.SET_NULL, blank=True, null=True)
    Type = models.CharField(max_length=100, default="", blank=True)
    Action = models.CharField(max_length=100, default="", blank=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    comment = models.CharField(max_length=1024, default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id']
    def __str__(self): 
        return f"{self.UserServices.ServiceCode}"
