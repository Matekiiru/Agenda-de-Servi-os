const API_BASE = "http://localhost:8000";
const barber = JSON.parse(localStorage.getItem("barberLogged"));
const token = localStorage.getItem("accessToken");

if (!barber || !token) {
  window.location.href = "login.html";
}

document.getElementById("barberName").innerText = `Barbeiro: ${barber.name}`;

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
  if (!confirm("Deseja cancelar este agendamento?")) return;

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

    await loadAppointments();
  } catch (error) {
    alert(error.message);
  }
}

function logout() {
  localStorage.removeItem("barberLogged");
  localStorage.removeItem("accessToken");
  window.location.href = "login.html";
}

loadAppointments();
