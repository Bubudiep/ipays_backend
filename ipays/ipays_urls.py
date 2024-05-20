# chat/urls.py
from django.urls import path, include
from . import views
from django.contrib.auth.models import User
from rest_framework import routers

router = routers.DefaultRouter()
router.register("users", views.UserViewsets, basename="users")
router.register("Photos", views.PhotosViewsets, basename="Photos")
router.register("UserProfile", views.UserProfileViewsets, basename="UserProfile")
router.register("Services", views.ServicesViewsets, basename="Services")
router.register("UserServices", views.UserServicesViewsets, basename="UserServices")
router.register("US_Member", views.US_MemberViewsets, basename="US_Member")
router.register("US_Floor", views.US_FloorViewsets, basename="US_Floor")
router.register("US_Rooms", views.US_RoomsViewsets, basename="US_Rooms")
router.register("US_Desk", views.US_DeskViewsets, basename="US_Desk")
router.register("shopmenus", views.US_MenuViewsets, basename="shopmenus")
router.register("shopmenus_items", views.US_MenuItemsViewsets, basename="shopmenus")
router.register("US_MenuType", views.US_MenuTypeViewsets, basename="US_MenuType")
router.register("US_Orders", views.US_OrdersViewsets, basename="US_Orders")
router.register("US_OrdersDetails", views.US_OrdersDetailsViewsets, basename="US_OrdersDetails")
router.register("Voucher", views.VoucherViewsets, basename="Voucher")
router.register("US_History", views.US_HistoryViewsets, basename="US_History")
router.register("Ipays", views.IpaysViewsets, basename="Ipays")
urlpatterns = [
    path('oauth2-info/', views.AuthInfo.as_view()),
    path('', include(router.urls)),
]