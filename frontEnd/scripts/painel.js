const barber = JSON.parse(localStorage.getItem("barberLogged"));
const token = localStorage.getItem("accessToken");

if (!barber || !token) {
  window.location.href = "login.html";
}

// mostra nome
document.getElementById("barberName").innerText = `Barbeiro: ${barber.name}`;

// pegar dados atualizados
function getAppointments() {
  return JSON.parse(localStorage.getItem("appointments")) || [];
}

// salvar dados
function saveAppointments(data) {
  localStorage.setItem("appointments", JSON.stringify(data));
}

// calcula horário final (NOVO)
function calculateEnd(start, duration) {
  const [h, m] = start.split(":").map(Number);
  const date = new Date();
  date.setHours(h);
  date.setMinutes(m + duration);

  return date.toTimeString().slice(0, 5);
}

function loadAppointments() {
  const date = document.getElementById("date").value;
  const listDiv = document.getElementById("list");

  listDiv.innerHTML = "";

  let appointments = getAppointments();

  // filtra por barbeiro
  let filtered = appointments.filter((app) => app.barber === barber.id);

  // filtro opcional por data
  if (date) {
    filtered = filtered.filter((app) => app.date === date);
  }

  // ordena por data + horário
  filtered.sort((a, b) => {
    const d1 = new Date(`${a.date}T${a.start}`);
    const d2 = new Date(`${b.date}T${b.start}`);
    return d1 - d2;
  });

  if (filtered.length === 0) {
    listDiv.innerHTML = "<p class='empty'>Nenhum agendamento</p>";
    return;
  }

  filtered.forEach((app) => {
    const div = document.createElement("div");
    div.className = "appointment";

    const endTime = calculateEnd(app.start, app.duration);

    div.innerHTML = `
      <div>
        <div>👤 ${app.client || "Sem nome"}</div>
        <div>💼 ${app.service || "Serviço não informado"}</div>
        <div>📅 ${app.date}</div>
        <div>⏰ ${app.start} - ${endTime}</div>
      </div>
      <button onclick="cancelAppointment('${app.barber}', '${app.date}', '${app.start}')">
        Cancelar
      </button>
    `;

    listDiv.appendChild(div);
  });
}

// cancelar corretamente
function cancelAppointment(barberId, date, time) {
  if (!confirm("Deseja cancelar este agendamento?")) return;

  let appointments = getAppointments();

  const index = appointments.findIndex(
    (app) => app.barber === barberId && app.date === date && app.start === time,
  );

  if (index !== -1) {
    appointments.splice(index, 1);
    saveAppointments(appointments);
    loadAppointments();
  }
}

// logout
function logout() {
  localStorage.removeItem("barberLogged");
  localStorage.removeItem("accessToken");
  window.location.href = "login.html";
}

// carrega automaticamente
loadAppointments();
