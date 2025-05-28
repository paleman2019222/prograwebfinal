import { } from 'https://www.gstatic.com/firebasejs/10.11.0/firebase-app-compat.js';
import { } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-auth-compat.js"
// <script src="https://www.gstatic.com/firebasejs/10.11.0/firebase-app-compat.js"></script>
 // <script src="https://www.gstatic.com/firebasejs/10.11.0/firebase-auth-compat.js"></script>
const googleButton = document.getElementById("google-button");
    const firebaseConfig = {
      apiKey: "AIzaSyDaZ7FDXhf7oYqF5bicCMevQGtfmFvXbJc",
      authDomain: "finalprograweb.firebaseapp.com",
      projectId: "finalprograweb",
      storageBucket: "finalprograweb.appspot.com",
      messagingSenderId: "422643893851",
      appId: "1:422643893851:web:01d7ccc0cf1364c08b617e"
    };

   
    if (!firebase.apps.length) {
      firebase.initializeApp(firebaseConfig);
    }

    const auth = firebase.auth();

    function updateStatus(message) {
      document.getElementById('status').innerText = message;
    }
    googleButton.addEventListener("click",async()=>{login();});
    async function login() {
      try {
        updateStatus("Iniciando sesión...");

        const provider = new firebase.auth.GoogleAuthProvider();
        provider.addScope('email');
        provider.addScope('profile');
        provider.setCustomParameters({ prompt: 'select_account' });

        console.log("Iniciando popup...");
        const result = await auth.signInWithPopup(provider);
        console.log("Popup completado:", result);

        if (!result.user) {
          throw new Error("No se obtuvo usuario");
        }

        updateStatus("Obteniendo token...");
        const idToken = await result.user.getIdToken();
        console.log("Token obtenido:", idToken.substring(0, 50) + "...");

        updateStatus("Enviando al backend...");

          const response = await fetch("http://127.0.0.1:8000/accounts/firebase-login/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Accept": "application/json"
            },
            body: JSON.stringify({ idToken }),
            credentials: 'include'  // 👈 NECESARIO para que Django guarde la cookie
          });

        console.log("Response status:", response.status);

        if (!response.ok) {
          const errorText = await response.text();
          console.error("Error del servidor:", errorText);
          throw new Error(`Error del servidor: ${response.status} - ${errorText}`);
        }

        const data = await response.json();
        console.log("Backend response:", data);
        if (data.redirect) {
          window.location.href = data.redirect;
      }

       updateStatus("¡Login exitoso!");
window.location.href = "/accounts/home/";  // o la ruta a la que quieras redirigir

      } catch (error) {
        console.error("Error completo:", error);
        updateStatus("Error en login: " + error.message);

        if (error.code) {
          console.error("Código de error:", error.code);
          switch (error.code) {
            case 'auth/popup-closed-by-user':
              updateStatus("Login cancelado por el usuario");
              break;
            case 'auth/popup-blocked':
              updateStatus("Popup bloqueado. Permite popups para este sitio.");
              break;
            case 'auth/cancelled-popup-request':
              updateStatus("Popup cancelado");
              break;
            default:
              updateStatus("Error de autenticación: " + error.message);
          }
        }
      }
    }

    auth.onAuthStateChanged((user) => {
      if (user) {
        console.log("Usuario autenticado:", user.displayName, user.email);
      } else {
        console.log("Usuario no autenticado");
      }
    });