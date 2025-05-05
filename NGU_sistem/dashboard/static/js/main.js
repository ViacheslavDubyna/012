// main.js для головного дашборду НГУ

document.addEventListener('DOMContentLoaded', function () {
    // Ініціалізація карти
    var map = L.map('map', {
        center: [50.4501, 30.5234], // Київ, можна змінити на центр України
        zoom: 6
    });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '© OpenStreetMap'
    }).addTo(map);

    // Завантаження підрозділів НГУ
    fetch('/api/ngu_units')
        .then(response => response.json())
        .then(data => {
            data.units.forEach(unit => {
                L.marker([unit.lat, unit.lng], {icon: L.icon({iconUrl: '/static/img/ngu_emblem_original.svg', iconSize: [32,32]})})
                    .addTo(map)
                    .bindPopup(`<b>${unit.name}</b><br>${unit.description}`);
            });
        });

    // Завантаження маршрутів патрулювання
    fetch('/api/ngu_patrol_routes')
        .then(response => response.json())
        .then(data => {
            data.routes.forEach(route => {
                L.polyline(route.coordinates, {color: 'blue', weight: 3, dashArray: '5,10'}).addTo(map).bindPopup('Маршрут патруля');
            });
        });

    // Завантаження інцидентів
    fetch('/api/incidents/active')
        .then(response => response.json())
        .then(data => {
            data.incidents.forEach(incident => {
                L.circleMarker([incident.lat, incident.lng], {color: 'red', radius: 8})
                    .addTo(map)
                    .bindPopup(`<b>Інцидент:</b> ${incident.type}<br><b>Опис:</b> ${incident.description}`);
            });
            // Оновлення списку інцидентів
            const list = document.getElementById('incidents-list');
            if (list) {
                list.innerHTML = '';
                data.incidents.slice(0, 5).forEach(incident => {
                    const div = document.createElement('div');
                    div.className = 'incident-list-item';
                    div.innerHTML = `<b>${incident.type}</b> (${incident.date})<br>${incident.description}`;
                    list.appendChild(div);
                });
            }
        });

    // Оновлення ключових показників (можна реалізувати через API)
    // fetch('/api/dashboard/stats').then(...)
});