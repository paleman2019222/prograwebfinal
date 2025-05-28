# En tu proyecto_principal/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('accounts.urls')),  
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    #path('accounts/', include('core.urls')) 
]