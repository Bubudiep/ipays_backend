from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('chat/', include('ipays.urls')),  # new
    path('i/', include('ipays.ipays_urls')),  # new
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('', admin.site.urls),
]
