const API_BASE = "http://localhost:8000";

const services = {
  1: { duration: 30, name: "Corte" },
  2: { duration: 60, name: "Corte e Barba" },
  3: { duration: 15, name: "Barba" },
};

async function loadBarbers() {
  const select = document.getElementById("barber");

  try {
    const response = await fetch(`${API_BASE}/barbeiros`);
    const barbers = await response.json();

    select.innerHTML = "";

    if (barbers.length === 0) {
      select.innerHTML = '<option value="">Nenhum barbeiro cadastrado</option>';
      return;
    }

    barbers.forEach((barber) => {
      const option = document.createElement("option");
      option.value = barber.id;
      option.textContent = barber.nome;
      select.appendChild(option);
    });
  } catch (error) {
    console.error("Erro ao carregar barbeiros:", error);
    select.innerHTML = '<option value="">Erro ao carregar barbeiros</option>';
  }
}

async function loadAvailability() {
  const barber = document.getElementById("barber").value;
  const serviceId = document.getElementById("service").value;
  const date = document.getElementById("date").value;

  if (!barber) {
    alert("Escolha um barbeiro");
    return;
  }

  if (!serviceId) {
    alert("Escolha um serviço");
    return;
  }

  if (!date) {
    alert("Escolha uma data");
    return;
  }

  const { duration, name } = services[serviceId];

  await generateSlots(barber, date, duration, name, serviceId);
}

async function generateSlots(barber, date, duration, serviceName, serviceId) {
  const slotsDiv = document.getElementById("slots");
  slotsDiv.innerHTML = "";

  try {
    const response = await fetch(
      `${API_BASE}/agendamentos?barbeiro_id=${barber}&data=${date}`,
    );
    const appointments = await response.json();

    const startHour = 9;
    const endHour = 18;

    for (let h = startHour; h < endHour; h++) {
      for (let m of [0, 30]) {
        const slotStart = `${pad(h)}:${pad(m)}`;
        const start = new Date(`${date}T${slotStart}:00`);
        const end = new Date(start.getTime() + duration * 60000);

        if (
          end.getHours() > endHour ||
          (end.getHours() === endHour && end.getMinutes() > 0)
        ) {
          continue;
        }

        const isBusy = appointments.some((app) => {
          const appStart = new Date(`${app.data}T${app.horario_inicio}`);
          const appEnd = new Date(appStart.getTime() + app.duracao * 60000);

          return start < appEnd && end > appStart;
        });

        const div = document.createElement("div");
        div.className = "slot";
        div.innerText = `${slotStart}`;

        if (isBusy) {
          div.style.background = "#7f1d1d";
          div.innerText += " (ocupado)";
        } else {
          div.style.background = "#065f46";
          div.innerText += " (livre)";

          div.onclick = async () => {
            const client = prompt("Nome do cliente:");

            if (!client || client.trim() === "") {
              alert("Nome inválido");
              return;
            }

            try {
              const response = await fetch(`${API_BASE}/agendamentos`, {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({
                  barbeiro_id: Number(barber),
                  cliente_nome: client.trim(),
                  servico_id: Number(serviceId),
                  data: date,
                  horario_inicio: slotStart,
                }),
              });

              const data = await response.json();

              if (!response.ok) {
                const detail = data.detail;
                const message =
                  typeof detail === "string"
                    ? detail
                    : Array.isArray(detail)
                      ? detail.map((item) => item.msg).join("; ")
                      : detail?.message || "Não foi possível agendar";

                throw new Error(message);
              }

              alert("Agendado!");
              await generateSlots(
                barber,
                date,
                duration,
                serviceName,
                serviceId,
              );
            } catch (error) {
              alert(error.message);
            }
          };
        }

        slotsDiv.appendChild(div);
      }
    }
  } catch (error) {
    console.error("Erro ao carregar horários:", error);
    slotsDiv.innerHTML = "<p>Erro ao carregar horários.</p>";
  }
}

function pad(n) {
  return n.toString().padStart(2, "0");
}

loadBarbers();
