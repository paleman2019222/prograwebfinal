from .models import Post, Reaction
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
import json
import firebase_admin
from firebase_admin import auth as firebase_auth, credentials

# Inicializar Firebase si no está ya inicializado
if not firebase_admin._apps:
    cred = credentials.Certificate("finalprograweb-firebase-adminsdk-fbsvc-b8a8adfa45.json")
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
            request.session['usuario_autenticado'] = True
            return JsonResponse({'message': 'Login exitoso', 'redirect': '/home/'})
             

        except Exception as e:
            print(f"Error en login_firebase: {e}")
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


@login_required
def logout_view(request):
    logout(request)
    return redirect('/accounts') 


@login_required
def ver_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    reacciones = {
    'like': '👍',    
    'hands': '🙌',
    'fire': '🔥',
    'wow': '😲',
}

    conteo_reacciones = []
    for tipo, emoji in reacciones.items():
        cantidad = Reaction.objects.filter(post=post, type=tipo).count()
        conteo_reacciones.append((emoji, cantidad))

    return render(request, 'ver_post.html', {
        'post': post,
        'conteo_reacciones': conteo_reacciones,
        'reacciones': reacciones,
        'csrf_token': get_token(request),
    })

@require_POST
@login_required
def reaccionar_post(request, post_id):
    try:
        data = json.loads(request.body)
        tipo_reaccion = data.get('type')

        if tipo_reaccion not in dict(Reaction.REACTION_CHOICES):
            return JsonResponse({'error': 'Tipo de reacción inválido'}, status=400)

        post = get_object_or_404(Post, id=post_id)

        reaction, created = Reaction.objects.get_or_create(
            user=request.user,
            post=post,
            type=tipo_reaccion
        )

        if not created:
            reaction.delete()
            return JsonResponse({'status': 'removed'})
        return JsonResponse({'status': 'added'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
    #Para la vista del perfil del usuario jeje
@login_required
def perfil_usuario(request):
    usuario = request.user
    posts_usuario = Post.objects.filter(author=usuario).order_by('-created_at')
    return render(request, 'perfil.html', {
        'usuario': usuario,
        'posts': posts_usuario
    })
#para editar el post en base al perfil
@login_required
def editar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content').strip()
        post.save()
        return redirect('perfil')

    return render(request, 'editar_post.html', {'post': post})
#para eliminar un post
@login_required
def eliminar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return redirect('perfil')
