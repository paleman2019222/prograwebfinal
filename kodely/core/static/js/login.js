import { GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-auth.js";
import { auth } from "./firebase-init.js";

const googleButton = document.getElementById("google-button");
const statusElement = document.getElementById("status");

function updateStatus(message) {
    if (statusElement) {
        statusElement.innerText = message;
    }
}

if (googleButton) {
    googleButton.addEventListener("click", async () => { login(); });
}
async function login() {
    try {
        updateStatus("Iniciando sesión...");

        const provider = new GoogleAuthProvider();
        provider.addScope('email');
        provider.addScope('profile');
        provider.setCustomParameters({ prompt: 'select_account' });

        console.log("Iniciando popup...");
        const result = await signInWithPopup(auth, provider);
        console.log("Popup completado:", result);

        if (!result.user) {
            throw new Error("No se obtuvo usuario");
        }

        updateStatus("Obteniendo token...");
        const idToken = await result.user.getIdToken();
        console.log("Token obtenido:", idToken.substring(0, 50) + "...");

        updateStatus("Enviando al backend...");

        const response = await fetch("http://localhost:8000/accounts/firebase-login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({ idToken })
        });

        console.log("Response status:", response.status);

        if (!response.ok) {
            const errorText = await response.text();
            console.error("Error del servidor:", errorText);
            throw new Error(`Error del servidor: ${response.status} - ${errorText}`);
        }

        const data = await response.json();
        console.log("Backend response:", data);

        updateStatus("¡Login exitoso!");
        alert("¡Bienvenido " + (data.user?.name || result.user.displayName) + "!");

        if (data.redirect) {
            window.location.href = data.redirect;
        } else {
            updateStatus("Login exitoso, pero sin redirección.");
        }

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