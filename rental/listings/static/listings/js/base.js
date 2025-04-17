document.addEventListener('DOMContentLoaded', function() {
    const dropdown = document.querySelector('.header-dropdown');
    const dropdownToggle = dropdown.querySelector('a');
    const dropdownMenu = dropdown.querySelector('.header-dropdown-menu');

    dropdownToggle.addEventListener('click', function(e) {
        e.preventDefault();
        if (dropdownMenu.style.display === 'block') {
            dropdownMenu.style.display = 'none';
        } else {
            dropdownMenu.style.display = 'block';
        }
    });

    dropdown.addEventListener('mouseenter', function() {
        dropdownMenu.style.removeProperty('display');
    });

    document.addEventListener('click', function(e) {
        if (!dropdown.contains(e.target)) {
            dropdownMenu.style.removeProperty('display');
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function (alert) {
            alert.style.transition = "opacity 0.5s ease";
            alert.style.opacity = "0";
            setTimeout(function () {
                alert.style.display = "none";
            }, 500);
        });
    }, 5000);
});