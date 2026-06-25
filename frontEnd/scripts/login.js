async function login() {
  const user = document.getElementById("user").value;
  const pass = document.getElementById("pass").value;

  try {
    const response = await fetch("http://localhost:8000/usuarios/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        username: user,
        password: pass,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Login inválido");
    }

    localStorage.setItem("barberLogged", JSON.stringify(data.barbeiro));
    localStorage.setItem("accessToken", data.access_token);

    window.location.href = "painel.html";
  } catch (error) {
    alert(error.message);
  }
}
