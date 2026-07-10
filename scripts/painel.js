const API_BASE = "http://3.85.94.102:8000";
const barber = JSON.parse(localStorage.getItem("barberLogged"));
const token = localStorage.getItem("accessToken");
const loginTime = Number(localStorage.getItem("loginTime") || 0);
const SESSION_LIMIT_MS = 60_000;

function showPopup(message, type = "info", duration = 0, options = {}) {
  const overlay = document.getElementById("popupOverlay");
  const box = document.getElementById("popupBox");
  const icon = document.getElementById("popupIcon");
  const msg = document.getElementById("popupMessage");
  const close = document.getElementById("popupClose");

  const {
    buttonText = "Fechar",
    onClose = null,
    closeOnOverlay = true,
  } = options;

  msg.textContent = message;
  box.dataset.type = type;
  close.textContent = buttonText;

  const icons = {
    success: "✅",
    error: "❌",
    info: "ℹ️",
  };

  icon.textContent = icons[type] || icons.info;
  overlay.classList.remove("hidden");

  close.onclick = () => {
    overlay.classList.add("hidden");
    if (onClose) {
      onClose();
    }
  };

  overlay.onclick = (event) => {
    if (event.target === overlay && closeOnOverlay) {
      overlay.classList.add("hidden");
      if (onClose) {
        onClose();
      }
    }
  };

  if (duration > 0) {
    setTimeout(() => {
      overlay.classList.add("hidden");
    }, duration);
  }
}

function confirmPopup(message) {
  return new Promise((resolve) => {
    const overlay = document.getElementById("popupOverlay");
    const box = document.getElementById("popupBox");
    const icon = document.getElementById("popupIcon");
    const msg = document.getElementById("popupMessage");
    const close = document.getElementById("popupClose");

    msg.textContent = message;
    box.dataset.type = "info";
    icon.textContent = "❓";

    close.textContent = "Cancelar";
    close.onclick = () => {
      overlay.classList.add("hidden");
      resolve(false);
    };

    const confirmButton = document.createElement("button");
    confirmButton.className = "popup-button";
    confirmButton.style.marginLeft = "8px";
    confirmButton.textContent = "Confirmar";

    const existingButton = close;
    existingButton.parentNode.insertBefore(
      confirmButton,
      existingButton.nextSibling,
    );

    confirmButton.onclick = () => {
      overlay.classList.add("hidden");
      confirmButton.remove();
      close.textContent = "Fechar";
      resolve(true);
    };

    overlay.classList.remove("hidden");
  });
}

function checkSession() {
  if (!barber || !token) {
    showPopup("Faça login para acessar o painel.", "error");
    setTimeout(() => {
      window.location.href = "login.html";
    }, 1000);
    return false;
  }

  if (Date.now() - loginTime > SESSION_LIMIT_MS) {
    localStorage.removeItem("barberLogged");
    localStorage.removeItem("accessToken");
    localStorage.removeItem("loginTime");
    showPopup("Sessão expirada. Faça login novamente.", "error", 0, {
      buttonText: "Confirmar",
      closeOnOverlay: false,
      onClose: () => {
        window.location.href = "login.html";
      },
    });
    return false;
  }

  return true;
}

if (checkSession()) {
  document.getElementById("barberName").innerText = `Barbeiro: ${barber.name}`;
}

setInterval(() => {
  if (!checkSession()) {
    clearInterval(this);
  }
}, 1000);

function calculateEnd(start, duration) {
  const [h, m] = start.split(":").map(Number);
  const date = new Date();
  date.setHours(h);
  date.setMinutes(m + duration);

  return date.toTimeString().slice(0, 5);
}

async function loadAppointments() {
  const date = document.getElementById("date").value;
  const listDiv = document.getElementById("list");

  listDiv.innerHTML = "";

  try {
    const params = new URLSearchParams();
    params.append("barbeiro_id", barber.id);
    if (date) {
      params.append("data", date);
    }

    const response = await fetch(
      `${API_BASE}/agendamentos?${params.toString()}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );

    const appointments = await response.json();

    appointments.sort((a, b) => {
      const d1 = new Date(`${a.data}T${a.horario_inicio}`);
      const d2 = new Date(`${b.data}T${b.horario_inicio}`);
      return d1 - d2;
    });

    if (appointments.length === 0) {
      listDiv.innerHTML = "<p class='empty'>Nenhum agendamento</p>";
      return;
    }

    appointments.forEach((app) => {
      const div = document.createElement("div");
      div.className = "appointment";

      const endTime = calculateEnd(app.horario_inicio, app.duracao);

      div.innerHTML = `
        <div>
          <div>👤 ${app.cliente || "Sem nome"}</div>
          <div>💼 ${app.servico || "Serviço não informado"}</div>
          <div>📅 ${app.data}</div>
          <div>⏰ ${app.horario_inicio} - ${endTime}</div>
        </div>
        <button onclick="cancelAppointment(${app.id})">
          Cancelar
        </button>
      `;

      listDiv.appendChild(div);
    });
  } catch (error) {
    console.error("Erro ao carregar agendamentos:", error);
    listDiv.innerHTML = "<p class='empty'>Erro ao carregar agendamentos</p>";
  }
}

async function cancelAppointment(agendamentoId) {
  const confirmCancel = confirm("Deseja cancelar este agendamento?");

  if (!confirmCancel) return;

  try {
    const response = await fetch(`${API_BASE}/agendamentos/${agendamentoId}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Não foi possível cancelar");
    }

    showPopup("Agendamento cancelado com sucesso.", "success", 1500);
    await loadAppointments();
  } catch (error) {
    showPopup(error.message, "error");
  }
}

function logout() {
  localStorage.removeItem("barberLogged");
  localStorage.removeItem("accessToken");
  localStorage.removeItem("loginTime");

  showPopup("Logout realizado com sucesso.", "success", 2000);

  setTimeout(() => {
    window.location.href = "login.html";
  }, 2000);
}

if (barber && token && Date.now() - loginTime <= SESSION_LIMIT_MS) {
  loadAppointments();
}
