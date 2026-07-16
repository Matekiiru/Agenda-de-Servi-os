function decodeJwtPayload(token) {
  try {
    const [, payload] = token.split(".");
    if (!payload) return null;

    const normalized = payload.replace(/-/g, "+").replace(/_/g, "/");
    const padded = normalized.padEnd(
      normalized.length + ((4 - (normalized.length % 4)) % 4),
      "=",
    );
    const decoded = atob(padded);

    return JSON.parse(decoded);
  } catch (error) {
    console.error("Erro ao decodificar o token:", error);
    return null;
  }
}

function getTokenExpiresAt(token) {
  const payload = decodeJwtPayload(token);
  if (!payload || !payload.exp) return null;

  return Number(payload.exp) * 1000;
}

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

    const expiresAt =
      getTokenExpiresAt(data.access_token) || Date.now() + 60_000;

    localStorage.setItem("barberLogged", JSON.stringify(data.barbeiro));
    localStorage.setItem("accessToken", data.access_token);
    localStorage.setItem("loginTime", Date.now().toString());
    localStorage.setItem("tokenExpiresAt", expiresAt.toString());

    showPopup("Login realizado com sucesso!", "success", 2000);

    setTimeout(() => {
      window.location.href = "painel.html";
    }, 2000);
  } catch (error) {
    showPopup(error.message, "error");
  }
}
