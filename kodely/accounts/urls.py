from django.urls import path
from .views import login_page, login_firebase, home, create_post, ver_post, logout_view

urlpatterns = [
    path('', login_page, name='login'), 
    path('firebase-login/', login_firebase, name='firebase_login'),
    path('home/', home, name='home'),
    path('crear-post/', create_post, name='crear_post'),
    path('post/<int:post_id>/', ver_post, name='ver_post'),  
    path('logout/', logout_view, name='logout_view')
]
