function renderAppointments() {
  const barber = document.getElementById("barber").value;
  const date = document.getElementById("date").value;

  const listDiv = document.getElementById("appointmentsList");
  listDiv.innerHTML = "";

  const filtered = appointments.filter(
    (app) => app.barber === barber && app.date === date,
  );

  filtered.forEach((app) => {
    const div = document.createElement("div");
    div.className = "slot";
    div.style.background = "#1e293b";

    div.innerText = `${app.start} (${app.duration}min)`;

    const btn = document.createElement("button");
    btn.innerText = "Cancelar";

    btn.onclick = () => {
      cancelAppointment(app.barber, app.date, app.start);
    };

    div.appendChild(btn);
    listDiv.appendChild(div);
  });
}
