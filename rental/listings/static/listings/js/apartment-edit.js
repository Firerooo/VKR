document.addEventListener("DOMContentLoaded", function () {
    const cityInput = document.getElementById("id_city");
    const addressInput = document.getElementById("id_address");  
    
    cityInput.addEventListener("input", function () {
        addressInput.value = ""; 
    });
});
document.addEventListener("DOMContentLoaded", function () {
    // Получаем CSRF-токен из скрытого инпута, который генерируется {% csrf_token %}
    const csrfTokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrfToken = csrfTokenInput ? csrfTokenInput.value : "";
    
    document.querySelectorAll(".delete-photo-btn").forEach(function(button) {
      button.addEventListener("click", function () {
        const photoItem = this.closest(".photo-item");
        const photoId = photoItem.dataset.photoId;
  
        if (confirm("Удалить это фото?")) {
          fetch(`/delete-photo/${photoId}/`, {
            method: "POST",
            headers: {
              "X-CSRFToken": csrfToken,
              "Content-Type": "application/json"
            },
          }).then(response => {
            if (response.ok) {
              photoItem.remove();
            } else {
              alert("Ошибка при удалении фото.");
            }
          })
          .catch(error => {
            console.error("Ошибка запроса:", error);
            alert("Ошибка при удалении фото.");
          });
        }
      });
    });
  });