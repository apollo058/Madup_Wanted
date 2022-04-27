
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/amounts', include('amounts.urls')),
    path('api/clients', include('clients.urls')),
]
