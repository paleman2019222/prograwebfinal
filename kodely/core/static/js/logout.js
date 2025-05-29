// logout.js
import { signOut } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-auth.js";
import { auth } from "./firebase-init.js";

const logoutButton = document.getElementById("logout-button");

async function logout() {
    try {
        await signOut(auth);
        await fetch("http://localhost:8000/accounts/logout", {

            method: "GET",
            //credentials: 'include'  // 👈 NECESARIO para que Django elimine la cookie
        });
        window.location.href = "/accounts";
    } catch (error) {
        console.error("Error cerrando sesión:", error);
    }
}

if (logoutButton) {
    logoutButton.addEventListener("click", async () => {
        await logout();
    });
} 