from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('app/', include('firstapp.urls')),
    path('admin/', admin.site.urls),
    path('', include('cms.urls')),
    path('cms/', include('cms.urls')),
]