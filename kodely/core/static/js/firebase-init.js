
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyDaZ7FDXhf7oYqF5bicCMevQGtfmFvXbJc",
    authDomain: "finalprograweb.firebaseapp.com",
    projectId: "finalprograweb",
    storageBucket: "finalprograweb.appspot.com",
    messagingSenderId: "422643893851",
    appId: "1:422643893851:web:01d7ccc0cf1364c08b617e"
};

export const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);

