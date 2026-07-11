function showPopup(message, type = "info", duration = 0) {
  const overlay = document.getElementById("popupOverlay");
  const box = document.getElementById("popupBox");
  const icon = document.getElementById("popupIcon");
  const msg = document.getElementById("popupMessage");
  const close = document.getElementById("popupClose");

  msg.textContent = message;
  box.dataset.type = type;

  const icons = {
    success: "✅",
    error: "❌",
    info: "ℹ️",
  };

  icon.textContent = icons[type] || icons.info;
  close.textContent = "Fechar";
  overlay.classList.remove("hidden");

  close.onclick = () => {
    overlay.classList.add("hidden");
  };

  overlay.onclick = (event) => {
    if (event.target === overlay) {
      overlay.classList.add("hidden");
    }
  };

  if (duration > 0) {
    setTimeout(() => {
      overlay.classList.add("hidden");
    }, duration);
  }
}

async function login() {
  const user = document.getElementById("user").value.trim();
  const pass = document.getElementById("pass").value;

  if (!user || !pass) {
    showPopup("Preencha usuário e senha para continuar.", "error");
    return;
  }

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
    localStorage.setItem("loginTime", Date.now().toString());

    showPopup("Login realizado com sucesso!", "success", 2000);

    setTimeout(() => {
      window.location.href = "painel.html";
    }, 2000);
  } catch (error) {
    showPopup(error.message, "error");
  }
}
