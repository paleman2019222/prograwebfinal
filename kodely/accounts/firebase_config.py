import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("finalprograweb-firebase-adminsdk-fbsvc-b8a8adfa45.json")  # Asegurate que la ruta sea correcta

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
