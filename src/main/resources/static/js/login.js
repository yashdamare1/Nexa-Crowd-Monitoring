
const loginForm = document.getElementById("loginForm");
const loginButton = document.getElementById("loginButton");
const loginError = document.getElementById("loginError");

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    loginError.textContent = "";
    loginButton.disabled = true;
    loginButton.textContent = "Signing in...";

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
            throw new Error(
                response.status === 401
                    ? "Invalid email or password."
                    : `Login failed (${response.status}).`
            );
        }

        const data = await response.json();

        if (!data.token) {
            throw new Error("The server did not return an authentication token.");
        }

        sessionStorage.setItem("nexaToken", data.token);
        sessionStorage.setItem("nexaName", data.name || data.email);
        sessionStorage.setItem("nexaRole", data.role || "");

        window.location.replace("/dashboard.html");
    } catch (error) {
        loginError.textContent = error.message || "Unable to connect to Nexa.";
    } finally {
        loginButton.disabled = false;
        loginButton.textContent = "Sign in";
    }
});
