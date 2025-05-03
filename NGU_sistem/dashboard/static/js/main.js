// Основний JavaScript файл для системи ДПСУ

// Ініціалізація карти при завантаженні сторінки
document.addEventListener('DOMContentLoaded', function() {
    // Перевіряємо, чи є на сторінці елемент для карти
    const mapElement = document.getElementById('map');
    if (mapElement) {
        initMap();
    }
});

// Функція ініціалізації карти
function initMap() {
    // Створюємо карту з центром на Україні
    const map = L.map('map').setView([49.0, 31.0], 6);

    // Додаємо тайли OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Завантажуємо дані про пункти пропуску та інциденти
    fetchMapData(map);
}

// Функція для завантаження даних для карти
function fetchMapData(map) {
    // Імітація даних для демонстрації (в реальній системі дані будуть завантажуватися з API)
    const checkpoints = [
        { id: 1, name: 'Краковець', lat: 49.9556, lng: 23.1333, type: 'автомобільний', status: 'активний' },
        { id: 2, name: 'Шегині', lat: 49.8167, lng: 23.0833, type: 'автомобільний', status: 'активний' },
        { id: 3, name: 'Рава-Руська', lat: 50.2500, lng: 23.6167, type: 'автомобільний', status: 'активний' },
        { id: 4, name: 'Ягодин', lat: 51.1833, lng: 23.9000, type: 'автомобільний', status: 'активний' },
        { id: 5, name: 'Чоп', lat: 48.4333, lng: 22.2000, type: 'залізничний', status: 'активний' }
    ];

    const incidents = [
        { id: 1, title: 'Спроба перетину кордону', lat: 50.1000, lng: 23.7000, type: 'порушення', severity: 'середня', status: 'активний' },
        { id: 2, title: 'Контрабанда товарів', lat: 49.8500, lng: 23.1500, type: 'контрабанда', severity: 'висока', status: 'вирішений' },
        { id: 3, title: 'Технічні проблеми на пункті пропуску', lat: 48.4500, lng: 22.2200, type: 'технічний', severity: 'низька', status: 'активний' }
    ];

    // Додаємо пункти пропуску на карту
    checkpoints.forEach(checkpoint => {
        const marker = L.marker([checkpoint.lat, checkpoint.lng], {
            icon: L.divIcon({
                className: 'checkpoint-marker',
                html: '<div></div>',
                iconSize: [12, 12]
            })
        }).addTo(map);

        marker.bindPopup(`
            <strong>${checkpoint.name}</strong><br>
            Тип: ${checkpoint.type}<br>
            Статус: ${checkpoint.status}
        `);
    });

    // Додаємо інциденти на карту
    incidents.forEach(incident => {
        const markerColor = incident.status === 'активний' ? 'red' : 'gray';
        
        const marker = L.marker([incident.lat, incident.lng], {
            icon: L.divIcon({
                className: 'incident-marker',
                html: `<div style="background-color: ${markerColor};"></div>`,
                iconSize: [12, 12]
            })
        }).addTo(map);

        marker.bindPopup(`
            <strong>${incident.title}</strong><br>
            Тип: ${incident.type}<br>
            Рівень загрози: ${incident.severity}<br>
            Статус: ${incident.status}
        `);
    });

    // Оновлюємо список останніх інцидентів
    updateIncidentsList(incidents);
}

// Функція для оновлення списку інцидентів
function updateIncidentsList(incidents) {
    const incidentsList = document.getElementById('incidents-list');
    if (!incidentsList) return;

    // Очищаємо список
    incidentsList.innerHTML = '';

    // Додаємо інциденти до списку
    incidents.forEach(incident => {
        const severityClass = {
            'низька': 'bg-success',
            'середня': 'bg-warning',
            'висока': 'bg-danger'
        }[incident.severity] || 'bg-secondary';

        const statusClass = {
            'активний': 'bg-danger',
            'вирішений': 'bg-success',
            'архівований': 'bg-secondary'
        }[incident.status] || 'bg-secondary';

        const incidentItem = document.createElement('div');
        incidentItem.className = 'incident-item';
        incidentItem.innerHTML = `
            <div><strong>${incident.title}</strong></div>
            <div>
                Тип: ${incident.type}
                <span class="badge ${severityClass}">${incident.severity}</span>
                <span class="badge ${statusClass}">${incident.status}</span>
            </div>
        `;

        incidentsList.appendChild(incidentItem);
    });
}