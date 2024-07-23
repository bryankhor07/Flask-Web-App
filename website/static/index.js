function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteImage(imageId) {
  fetch("/delete-image", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": "{{ csrf_token() }}", // Include CSRF token if using Flask-WTF
    },
    body: JSON.stringify({ imageId: imageId }),
  }).then((response) => {
    if (response.ok) {
      window.location.href = "/gallery";
    } else {
      alert("Failed to delete account");
    }
  });
}

function deleteAccount(userId) {
  fetch("/delete-account", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": "{{ csrf_token() }}", // Include CSRF token if using Flask-WTF
    },
    body: JSON.stringify({ userId: userId }),
  }).then((response) => {
    if (response.ok) {
      window.location.href = "/sign-up";
    } else {
      alert("Failed to delete account");
    }
  });
}

function deleteTask(taskId) {
  fetch("/delete-task", {
    method: "POST",
    body: JSON.stringify({ taskId: taskId }),
  }).then((_res) => {
    window.location.href = "/tasks";
  });
}

async function getWeather() {
  const city = document.getElementById("city").value;
  const response = await fetch(`/weather?city=${city}`);
  if (response.ok) {
    const data = await response.json();
    if (data.main && data.weather && data.wind && data.clouds) {
      document.getElementById("weather-result").innerHTML = `
        <h3>Weather in ${data.name}</h3>
        <p>Temperature: ${data.main.temp}°C</p>
        <p>Weather: ${data.weather[0].description}</p>
        <p>Humidity: ${data.main.humidity}%</p>
        <p>Wind speed: ${data.wind.speed} m/s</p>
        <p>Cloudiness: ${data.clouds.all}%</p>
        <p>Pressure: ${data.main.pressure} hPa</p>
      `;
    } else {
      alert("City not found");
    }
  }
}
