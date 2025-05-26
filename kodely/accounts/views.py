from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
import json
from firebase_admin import auth as firebase_auth

@csrf_exempt
def login_firebase(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_token = data.get('idToken')
            decoded_token = firebase_auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            name = decoded_token.get('name')
            email = decoded_token.get('email')

            return JsonResponse({
                'message': 'Usuario autenticado correctamente',
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
