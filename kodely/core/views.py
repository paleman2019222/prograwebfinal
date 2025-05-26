from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

def login_view(request):
    return render(request, 'login.html')

@csrf_exempt
@require_http_methods(["POST"])
def firebase_login(request):
    try:
        data = json.loads(request.body)
        id_token = data.get('idToken')
        
        if not id_token:
            return JsonResponse({'error': 'Token no proporcionado'}, status=400)
        
        # Por ahora solo retornamos éxito para probar
        # Más tarde aquí verificarías el token con Firebase Admin SDK
        return JsonResponse({
            'success': True,
            'user': {
                'name': 'Usuario de Prueba',
                'email': 'test@example.com'
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)