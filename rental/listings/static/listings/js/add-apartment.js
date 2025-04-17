function initAutocomplete() {
    // Элементы формы
    var cityInput = document.getElementById("id_city");
    var addressInput = document.getElementById("id_address");

    // Инициализация автодополнения для городов
    var cityAutocomplete = new google.maps.places.Autocomplete(cityInput, {
        types: ["(cities)"]
    });

    cityAutocomplete.addListener("place_changed", function () {
        var place = cityAutocomplete.getPlace();
        if (!place.address_components) {
            return;
        }

        // Извлекаем только название города
        var city = "";
        place.address_components.forEach(function (component) {
            if (component.types.indexOf("locality") !== -1) {
                city = component.long_name;
            }
        });

        // Записываем найденный город в поле
        cityInput.value = city;

        // Ограничиваем адресное автодополнение видимой областью выбранного города
        if (place.geometry && place.geometry.viewport) {
            addressAutocomplete.setBounds(place.geometry.viewport);
        }
    });

    // Инициализация автодополнения для адреса
    var addressAutocomplete = new google.maps.places.Autocomplete(addressInput, {
        types: ["address"]
    });

    addressAutocomplete.addListener("place_changed", function () {
        var place = addressAutocomplete.getPlace();
        if (!place.geometry) {
            return;
        }
        // Записываем координаты выбранного адреса
        document.getElementById("latitude").value = place.geometry.location.lat();
        document.getElementById("longitude").value = place.geometry.location.lng();
    });
    
    var statusInputs = document.querySelectorAll('input[name="status"]');
    var rentalWrapper = document.getElementById('rental_period_wrapper');

    function toggleRentalPeriod() {
        var selected = Array.from(statusInputs).find(function(input) {
            return input.checked;
        });
        if (selected && selected.value === "RENT") {
            rentalWrapper.style.display = "block";
        } else {
            rentalWrapper.style.display = "none";
        }
    }

    toggleRentalPeriod();

    statusInputs.forEach(function(input) {
        input.addEventListener('change', toggleRentalPeriod);
    });
}

// Запускаем автозаполнение, когда страница полностью загружена
google.maps.event.addDomListener(window, "load", initAutocomplete);
