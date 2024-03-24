from django.contrib import admin
from .models import *

admin.site.register(Room)
admin.site.register(Message)

@admin.register(Photos)
class PhotosAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 
    "file_name",
    "file_type",
    "file_size",
    "img_tag",
    "Comment",
    "user",
    "created",
    "updated"]
    search_fields = ['file_name']
    list_editable = ['file_name']
    list_filter = ['file_type']
    raw_id_fields = ["user"]
    readonly_fields = ["user","img_tag"]
    save_as = True

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 
    "ServiceCode",
    "ServiceName",
    "created",
    "updated"]
    search_fields = ['ServiceCode']
    save_as = True

@admin.register(UserServices)
class UserServicesAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 
    "ServiceCode",
    "Name",
    "Status",
    "user",
    "Hotline",
    "Zalo",
    "Facebook",
    "IsPublic",
    "comment",
    "created",
    "updated"]
    search_fields = ['Name','user']
    list_editable = []
    list_filter = ['Status','IsPublic']
    raw_id_fields = ["user","ServiceCode"]
    save_as = True

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 
    "user",
    "level",
    "fullname",
    "birthday",
    "adr_tinh",
    "adr_thanhpho",
    "adr_huyen",
    "adr_xa",
    "comment",
    "created",
    "updated"]
    search_fields = ['user']
    list_editable = ['comment']
    list_filter = ['user','adr_tinh','adr_thanhpho','adr_huyen','adr_xa']
    raw_id_fields = ['user']
    readonly_fields = []
    save_as = True
