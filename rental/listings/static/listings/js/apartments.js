document.addEventListener("DOMContentLoaded", async function() {
    const cityInput = document.getElementById("city-search");
    const autocompleteList = document.getElementById("autocomplete-list");
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

    // Обработчики для выпадающих меню
    dropdownToggles.forEach(function (toggle) {
        toggle.addEventListener('click', function (e) {
            const allMenus = document.querySelectorAll('.dropdown-menu');
            allMenus.forEach(function (menu) {
                if (menu !== toggle.nextElementSibling) {
                    menu.style.display = 'none';
                }
            });
            const dropdownMenu = toggle.nextElementSibling;
            dropdownMenu.style.display = (dropdownMenu.style.display === 'block') ? 'none' : 'block';
            e.stopPropagation();
        });
    });

    document.addEventListener('click', function (event) {
        if (!event.target.closest('.dropdown-container')) {
            document.querySelectorAll('.dropdown-menu').forEach(function (menu) {
                menu.style.display = 'none';
            });
        }
    });

    // При фокусе на поисковом поле сразу отобразить полный список городов
    cityInput.addEventListener("focus", function() {
        if (cityInput.value.trim() === "") {
            fetch(`/get_cities/?q=`)
                .then(response => response.json())
                .then(data => {
                    autocompleteList.innerHTML = "";
                    data.cities.forEach(city => {
                        const option = document.createElement("div");
                        option.textContent = city;
                        option.classList.add("autocomplete-item");
                        option.onclick = function() {
                            cityInput.value = city;
                            autocompleteList.innerHTML = "";
                        };
                        autocompleteList.appendChild(option);
                    });
                });
        }
    });
    
    // Поле ввода города с автодополнением при вводе 2-х и более символов
    cityInput.addEventListener("input", function() {
        const query = cityInput.value.trim();
        if (query.length < 2) {
            autocompleteList.innerHTML = "";
            return;
        }
    
        fetch(`/get_cities/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                autocompleteList.innerHTML = "";
                data.cities.forEach(city => {
                    const option = document.createElement("div");
                    option.textContent = city;
                    option.classList.add("autocomplete-item");
                    option.onclick = function() {
                        cityInput.value = city;
                        autocompleteList.innerHTML = "";
                    };
                    autocompleteList.appendChild(option);
                });
            });
    });
    
    document.addEventListener("click", function(event) {
        if (!cityInput.contains(event.target) && !autocompleteList.contains(event.target)) {
            autocompleteList.innerHTML = "";
        }
    });

    // Карта и маркеры
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: { lat: 55.7558, lng: 37.6173 }, 
        mapId: MAP_ID
    });

    // Загружаем маркерные данные из шаблона
    const markersData = JSON.parse(document.getElementById('markers_data').textContent);
    console.log("Markers array:", markersData);

    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

    // Создаём LatLngBounds для автоматического определения границ
    const bounds = new google.maps.LatLngBounds();

    markersData.forEach(markerData => {
        const currencyMapping = {
            "RUB": "₽",
            "USD": "$",
            "EUR": "€"
        };
    
        const rentalPeriodMapping = {
            "DAILY": "сут.",
            "MONTHLY": "мес."
        };
    
        // Формируем текст для вывода цены
        let priceText = "";
        if (markerData.price) {
            // Получаем сокращённое название валюты; если не найдено – приводим исходное значение к нижнему регистру
            let currencyText = currencyMapping[markerData.currency] || (markerData.currency ? markerData.currency.toLowerCase() : "руб");
            priceText = markerData.price + " " + currencyText;
    
            // Если статус объявления - аренда и задан период сдачи, добавляем информацию о периоде
            if (markerData.status === "RENT" && markerData.rental_period) {
                let periodText = rentalPeriodMapping[markerData.rental_period] || markerData.rental_period.toLowerCase();
                priceText += " / " + periodText;
            }
        }
    
        // Создаём элемент маркера с сформированным текстом
        const markerContent = document.createElement("div");
        markerContent.classList.add("custom-marker");
        markerContent.innerText = priceText;
    
        const markerPosition = { lat: markerData.lat, lng: markerData.lng };
        bounds.extend(markerPosition);
    
        const marker = new AdvancedMarkerElement({
            map: map,
            position: markerPosition,
            title: priceText ? `Цена: ${priceText}` : "Без цены",
            content: markerContent
        });
    
        marker.addListener("click", () => {
            window.location.href = `/apartment/${markerData.id}/`;
        });
    });

    // Устанавливаем центр и зум карты на основе границ
    if (!bounds.isEmpty()) {
        if (markersData.length === 1) {
            map.setCenter(bounds.getCenter());
            map.setZoom(17);
        } else {
            map.fitBounds(bounds);
        }
    }
    document.addEventListener("DOMContentLoaded", function () {
        const statusRadios = document.querySelectorAll('input[name="status"]');
        statusRadios.forEach(function(radio) {
          radio.addEventListener("change", function () {
            document.getElementById("filter-form").submit();
          });
        });
      });

  const statusRadios = document.querySelectorAll('input[name="status"]');
  
  statusRadios.forEach(function(radio) {
    radio.addEventListener("change", function () {
      document.getElementById("filter-form").submit();
    });
  });

  document.getElementById('reset-filters').addEventListener('click', function(){
    const form = document.getElementById('filter-form');

    form.querySelectorAll('input[type="text"], input[type="number"]').forEach(input => {
      input.value = "";
    });
    
    ["currency", "rental_period"].forEach(name => {
        form.querySelectorAll('input[name="' + name + '"]').forEach(radio => {
          radio.checked = (radio.value === "");
        });
      });
    
    form.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
      checkbox.checked = false;
    });
    
    document.querySelectorAll('.toggle-option').forEach(opt => {
      opt.classList.remove('active');
    });
    
    form.submit();
  });
});
