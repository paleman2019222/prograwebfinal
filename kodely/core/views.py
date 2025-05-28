from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import get_user_model, login
import json

# Firebase Admin SDK
import firebase_admin
from firebase_admin import auth as firebase_auth, credentials

# Inicializa Firebase solo una vez
if not firebase_admin._apps:
    cred = credentials.Certificate("finalprograweb-firebase-adminsdk-fbsvc-b8a8adfa45.json")  # ← Asegurate que el JSON esté ahí
    firebase_admin.initialize_app(cred)

# Tu modelo CustomUser
User = get_user_model()

@csrf_exempt
def login_firebase(request):
    if request.method == 'POST':
        try:
            # Leer token enviado desde el frontend
            data = json.loads(request.body)
            id_token = data.get('idToken')
            decoded_token = firebase_auth.verify_id_token(id_token)

            # Datos del usuario desde Firebase
            uid = decoded_token['uid']
            name = decoded_token.get('name', '')
            email = decoded_token.get('email', '')

            # Crear o recuperar el usuario usando el modelo personalizado
            user, created = User.objects.get_or_create(
                username=uid,
                defaults={
                    'email': email,
                    'name': name,  # 👈 Asegurate que tu CustomUser tenga un campo llamado "name"
                }
            )

            # Iniciar sesión en Django
            login(request, user)

            return JsonResponse({
                'message': 'Usuario autenticado correctamente',
                'created': created,
                'user': {
                    'uid': uid,
                    'name': name,
                    'email': email
                }
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def login_page(request):
    return render(request, "login.html")

def home(request):
    return render(request, 'home.html') 
