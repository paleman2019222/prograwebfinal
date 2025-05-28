from django.urls import path
from .views import login_page, login_firebase, home

urlpatterns = [
    path('', login_page, name='login'), 
    path('firebase-login/', login_firebase, name='firebase_login'),
    path('home/', home, name='home'),
]