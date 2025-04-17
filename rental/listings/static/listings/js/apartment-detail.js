let currentIndex = 0;
const slide = document.getElementById('carouselSlide');
const images = slide.querySelectorAll('img');
const total = images.length;

function moveSlide(direction) {
  currentIndex = (currentIndex + direction + total) % total;
  slide.style.transform = `translateX(-${currentIndex * 100}vw)`;
}
(async function() {
// Создаем карту
const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: { lat: 55.7558, lng: 37.6173 },
    mapId: MAP_ID
});

// Получаем данные маркера из JSON, переданного шаблоном
const markersData = JSON.parse(document.getElementById("markers_data").textContent);
console.log("Markers data:", markersData);

if (markersData.length > 0) {
    const markerData = markersData[0];  // так как у нас всегда один маркер

    // Создаем контент для кастомного маркера
    const markerContent = document.createElement("div");
    markerContent.classList.add("custom-marker");
    markerContent.innerText = markerData.price ? markerData.price + " руб./сут." : "";

    const markerPosition = { lat: markerData.lat, lng: markerData.lng };

    // Импортируем библиотеку маркеров Google Maps
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

    // Добавляем кастомный маркер на карту
    new AdvancedMarkerElement({
    map: map,
    position: markerPosition,
    title: markerData.price ? `Цена: ${markerData.price} руб./сут.` : "Без цены",
    content: markerContent
    });

    // Центрируем карту на маркере и устанавливаем нужный зум
    map.setCenter(markerPosition);
    map.setZoom(16);
}
})();
document.addEventListener("DOMContentLoaded", function () {
// Выбираем все изображения, открывающие модальное окно. Проверьте, что у них установлен класс "thumbnail".
const photoNodes = document.querySelectorAll(".thumbnail");
if (photoNodes.length === 0) {
console.warn("Элементы с классом 'thumbnail' не найдены. Проверьте, что изображения имеют правильный класс.");
}

// Собираем массив URL фотографий
const photos = Array.from(photoNodes).map(img => img.src);

// Элементы модального окна
const modal = document.getElementById("photosModal");
// Используем тот же id, который указан в HTML для главного фото (например, photosModalMain)
const modalMainImg = document.getElementById("photosModalMain");
const modalThumbnailsContainer = document.getElementById("photosModalThumbnails");
const closeBtn = document.querySelector(".photos-modal .photos-modal-close");
const leftArrow = document.getElementById("modalLeftArrow");
const rightArrow = document.getElementById("modalRightArrow");

let currentIndex = 0;

// Функция обновления главного изображения и подсветки миниатюр
function updateModalImage(index) {
if (index < 0) index = photos.length - 1;
if (index >= photos.length) index = 0;
currentIndex = index;
modalMainImg.src = photos[currentIndex];

// Обновляем класс active у миниатюр
const thumbImages = modalThumbnailsContainer.querySelectorAll("img");
thumbImages.forEach((thumb, idx) => {
    thumb.classList.toggle("active", idx === currentIndex);
});
}

// Функция открытия модального окна
function openModal(index) {
currentIndex = index;
updateModalImage(currentIndex);
// Заполняем контейнер миниатюр динамически
modalThumbnailsContainer.innerHTML = "";
photos.forEach((src, idx) => {
    const thumb = document.createElement("img");
    thumb.src = src;
    if (idx === currentIndex) thumb.classList.add("active");
    thumb.addEventListener("click", function () {
    updateModalImage(idx);
    });
    modalThumbnailsContainer.appendChild(thumb);
});
modal.style.display = "block";
}

// Функция закрытия модального окна
function closeModal() {
modal.style.display = "none";
}

// Обработчики стрелок
leftArrow.addEventListener("click", function (e) {
e.stopPropagation();
updateModalImage(currentIndex - 1);
});
rightArrow.addEventListener("click", function (e) {
e.stopPropagation();
updateModalImage(currentIndex + 1);
});

// Обработчик закрытия окна по клику на крестик
closeBtn.addEventListener("click", function () {
closeModal();
});

// Закрытие, если клик вне содержимого модального окна
modal.addEventListener("click", function (e) {
if (e.target === modal) {
    closeModal();
}
});

// Привязываем открытие модального окна к клику по фотографии
photoNodes.forEach((img, index) => {
img.style.cursor = "pointer";
img.addEventListener("click", function () {
    openModal(index);
});
});
});
document.addEventListener("DOMContentLoaded", function () {
// Элементы формы и модального окна
const deleteButton = document.getElementById("deleteButton");
const deleteModal = document.getElementById("deleteModal");
const closeModal = document.querySelector(".delete-modal-close");
const cancelDelete = document.getElementById("cancelDelete");
const confirmDelete = document.getElementById("confirmDelete");
const deleteForm = document.getElementById("deleteForm");

// При клике на кнопку "Удалить" открываем модальное окно
deleteButton.addEventListener("click", function () {
    deleteModal.style.display = "block";
});

// Закрытие модального окна при клике на крестик или кнопку "Отмена"
closeModal.addEventListener("click", function () {
    deleteModal.style.display = "none";
});
cancelDelete.addEventListener("click", function () {
    deleteModal.style.display = "none";
});

// Если подтверждаем удаление, отправляем форму
confirmDelete.addEventListener("click", function () {
    deleteForm.submit();
});

// Закрытие модального окна при клике вне его содержимого
window.addEventListener("click", function (event) {
    if (event.target === deleteModal) {
    deleteModal.style.display = "none";
    }
});
});