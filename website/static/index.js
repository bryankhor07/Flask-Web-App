function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
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
