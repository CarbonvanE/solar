document.addEventListener('DOMContentLoaded', function() {
    const iconDiv = $('.weather-icon');
    fetch('/json/icon')
        .then(function(response) {
            return response.json();
        })
        .then(function(response) {
            iconDiv.html(`<i class="fas ${response['icon']} fa-lg"></i>`);
        })
});
