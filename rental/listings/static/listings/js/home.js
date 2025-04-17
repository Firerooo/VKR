document.addEventListener("DOMContentLoaded", function() {
    const cityInput = document.getElementById("homepage-city-search");
    const autocompleteList = document.getElementById("homepage-autocomplete-list");
    const searchBtn = document.getElementById("homepage-search-btn");

    // Функция для запроса списка городов
    function fetchCities(query) {
        fetch(getCitiesUrl + "?q=" + encodeURIComponent(query))
            .then(response => response.json())
            .then(data => {
                autocompleteList.innerHTML = "";
                data.cities.forEach(city => {
                    const option = document.createElement("div");
                    option.textContent = city;
                    option.classList.add("homepage-autocomplete-item");
                    option.onclick = function() {
                        cityInput.value = city;
                        autocompleteList.innerHTML = "";
                    };
                    autocompleteList.appendChild(option);
                });
            })
            .catch(err => console.error("Ошибка при получении городов:", err));
    }

    // При фокусе, если поле пустое – показать полный список городов
    cityInput.addEventListener("focus", function() {
        if (cityInput.value.trim() === "") {
            fetchCities("");
        }
    });

    // По мере ввода, если значение больше 2 символов, показываем список с фильтром
    cityInput.addEventListener("input", function() {
        const query = cityInput.value.trim();
        if (query.length < 2) {
            autocompleteList.innerHTML = "";
            return;
        }
        fetchCities(query);
    });

    // Скрываем выпадающий список, если клик вне поля и списка
    document.addEventListener("click", function(event) {
        if (!cityInput.contains(event.target) && !autocompleteList.contains(event.target)) {
            autocompleteList.innerHTML = "";
        }
    });

    // При клике на кнопку «Поиск» перенаправляем на страницу объявлений,
    // передавая введённый город через GET-параметр 'city'
    searchBtn.addEventListener("click", function() {
        const city = cityInput.value.trim();
        window.location.href = apartmentsUrl + "?city=" + encodeURIComponent(city);
    });
});
