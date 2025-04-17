function initCityAutocomplete() {
    var cityInput = document.getElementById("id_city");

    // Автодополнение для городов
    var cityAutocomplete = new google.maps.places.Autocomplete(cityInput, {
        types: ["(cities)"]
    });

    cityAutocomplete.addListener("place_changed", function () {
        var place = cityAutocomplete.getPlace();
        if (!place.address_components) {
            return;
        }

        var city = "";
        place.address_components.forEach(function (component) {
            if (component.types.includes("locality")) { 
                city = component.long_name; // Извлекаем только название города
            }
        });

        // Устанавливаем название города в поле ввода
        cityInput.value = city;
    });
}

// Запускаем автодополнение при загрузке страницы
google.maps.event.addDomListener(window, "load", initCityAutocomplete);
