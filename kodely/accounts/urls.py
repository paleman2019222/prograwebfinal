from django.urls import path

from .views import login_page, login_firebase, home, create_post, ver_post, logout_view

from . import views
#from django.urls import path
#from . import views


urlpatterns = [
    path('',home, name='home'), 
    path('firebase-login/', login_firebase, name='firebase_login'),
    path('home/', home, name='home'),
    path('crear-post/', create_post, name='crear_post'),
 
    path('logout/', logout_view, name='logout_view'),
    path('login/', login_page, name='login_page'),

    path('post/<int:post_id>/', ver_post, name='ver_post'), 
    path('accounts/reaccionar/<int:post_id>/', views.reaccionar_post, name='reaccionar_post'),
     path('perfil/', views.perfil_usuario, name='perfil'),
    path('editar/<int:post_id>/', views.editar_post, name='editar_post'),
    path('eliminar/<int:post_id>/', views.eliminar_post, name='eliminar_post'), 
]
