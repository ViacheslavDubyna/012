// Основні JavaScript функції для інформаційно-аналітичної системи Національної гвардії України

// Функція для ініціалізації графіків на сторінках
function initCharts() {
    // Перевіряємо наявність контейнерів для графіків на сторінці
    if (document.getElementById('incidentsByTypeChart')) {
        initIncidentsByTypeChart();
    }
    
    if (document.getElementById('incidentsBySeverityChart')) {
        initIncidentsBySeverityChart();
    }
    
    if (document.getElementById('threatByRegionChart')) {
        initThreatByRegionChart();
    }
    
    if (document.getElementById('resourceAllocationChart')) {
        initResourceAllocationChart();
    }
}

// Функція для ініціалізації карти на сторінках
function initMap() {
    // Перевіряємо наявність контейнера для карти на сторінці
    const mapContainer = document.getElementById('map');
    if (mapContainer) {
        // Ініціалізуємо карту з центром на Україні
        const map = L.map('map').setView([49.0, 31.0], 6);
        
        // Додаємо шар OpenStreetMap
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
        
        // Повертаємо об'єкт карти для подальшого використання
        return map;
    }
    return null;
}

// Функція для завантаження даних з API
function fetchData(endpoint, callback) {
    fetch(endpoint)
        .then(response => {
            if (!response.ok) {
                throw new Error('Помилка завантаження даних');
            }
            return response.json();
        })
        .then(data => {
            callback(data);
        })
        .catch(error => {
            console.error('Помилка завантаження даних:', error);
        });
}

// Ініціалізуємо функціональність при завантаженні сторінки
document.addEventListener('DOMContentLoaded', function() {
    initCharts();
    initMap();
});