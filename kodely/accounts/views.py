from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from .models import Post
import json


import firebase_admin
from firebase_admin import auth as firebase_auth, credentials


if not firebase_admin._apps:
    cred = credentials.Certificate("finalprograweb-firebase-adminsdk-fbsvc-b8a8adfa45.json")  # ← Asegurate que el JSON esté ahí
    firebase_admin.initialize_app(cred)


User = get_user_model()

@csrf_exempt
def login_firebase(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_token = data.get('idToken')

            decoded_token = firebase_auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            name = decoded_token.get('name', '')
            email = decoded_token.get('email')
            photo_url = decoded_token.get('picture', '')

           
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'uid': uid,
                    'name': name,
                    'photo_url': photo_url
                }
            )

  
            login(request, user)
            print("LOGIN ejecutado. ¿User en sesión?", request.user.is_authenticated)
            request.session['usuario_autenticado'] = True  # fuerza creación de sesión
            return JsonResponse({'message': 'Login exitoso', 'redirect': '/home/'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

       

        post = Post.objects.create(
            title=title,
            content=content,
            author=request.user
        )
        return redirect('/home/') 
    return render(request, 'create_post.html')

def login_page(request):
    return render(request, "login.html")

def home(request):
    posts = Post.objects.all().order_by('-id')
    return render(request, 'home.html', {'posts': posts})

@login_required
def ver_post(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'ver_post.html', {'post': post})