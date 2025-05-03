/**
 * Скрипт для відображення карти інцидентів та роботи з фільтрами
 * 
 * Цей файл містить функції для ініціалізації карти інцидентів,
 * завантаження даних про інциденти та роботи з фільтрами
 */

document.addEventListener('DOMContentLoaded', function() {
    // Ініціалізуємо карту інцидентів
    initIncidentsMap();
    
    // Ініціалізуємо фільтри
    initIncidentsFilter();
});

/**
 * Ініціалізація карти інцидентів
 */
function initIncidentsMap() {
    // Перевіряємо, чи знаходимося ми на сторінці інцидентів
    const mapContainer = document.querySelector('.map-container');
    if (!mapContainer) return;
    
    // Очищаємо контейнер від тексту-заповнювача
    mapContainer.innerHTML = '';
    
    // Створюємо елемент для карти
    const mapElement = document.createElement('div');
    mapElement.id = 'incidents-map';
    mapElement.style.height = '100%';
    mapContainer.appendChild(mapElement);
    
    // Створюємо карту з центром на Україні
    const map = L.map('incidents-map').setView([49.0, 31.0], 6);
    
    // Додаємо тайли OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Завантажуємо дані про інциденти
    fetchIncidentsData(map);
}

/**
 * Завантаження даних про інциденти
 */
function fetchIncidentsData(map) {
    // В реальній системі дані будуть завантажуватися з API
    // Для демонстрації використовуємо тестові дані
    const testData = [
        {
            id: 1,
            title: 'Спроба незаконного перетину кордону',
            description: 'Група з 5 осіб намагалася незаконно перетнути кордон в районі пункту пропуску "Шегині".',
            priority: 'high',
            status: 'active',
            location: {
                lat: 49.8086,
                lng: 23.1314
            },
            timestamp: '2025-01-15T14:30:00'
        },
        {
            id: 2,
            title: 'Виявлення контрабанди',
            description: 'Виявлено спробу перевезення контрабандних товарів через пункт пропуску "Краковець".',
            priority: 'medium',
            status: 'active',
            location: {
                lat: 49.9556,
                lng: 23.1025
            },
            timestamp: '2025-01-15T11:15:00'
        },
        {
            id: 3,
            title: 'Порушення правил перетину кордону',
            description: 'Громадянин намагався перетнути кордон за підробленими документами в пункті пропуску "Ягодин".',
            priority: 'medium',
            status: 'active',
            location: {
                lat: 51.0775,
                lng: 23.9325
            },
            timestamp: '2025-01-14T16:45:00'
        }
    ];
    
    // Додаємо маркери на карту
    addIncidentsToMap(map, testData);
    
    // Оновлюємо список інцидентів
    updateIncidentsList(testData);
}

/**
 * Додавання інцидентів на карту
 */
function addIncidentsToMap(map, incidents) {
    // Створюємо групу для маркерів
    const markers = L.layerGroup().addTo(map);
    
    // Додаємо кожен інцидент як маркер на карту
    incidents.forEach(incident => {
        // Визначаємо колір маркера в залежності від пріоритету
        let markerColor;
        switch(incident.priority) {
            case 'high':
                markerColor = '#dc3545'; // червоний
                break;
            case 'medium':
                markerColor = '#ffc107'; // жовтий
                break;
            case 'low':
                markerColor = '#28a745'; // зелений
                break;
            default:
                markerColor = '#007bff'; // синій
        }
        
        // Створюємо HTML для маркера
        const markerHtml = `
            <div class="incident-marker">
                <div style="background-color: ${markerColor};"></div>
            </div>
        `;
        
        // Створюємо іконку для маркера
        const icon = L.divIcon({
            html: markerHtml,
            className: '',
            iconSize: [12, 12],
            iconAnchor: [6, 6]
        });
        
        // Створюємо маркер та додаємо його на карту
        const marker = L.marker([incident.location.lat, incident.location.lng], {
            icon: icon
        }).addTo(markers);
        
        // Додаємо спливаюче вікно з інформацією про інцидент
        marker.bindPopup(`
            <h6>${incident.title}</h6>
            <p>${incident.description}</p>
            <small>Пріоритет: ${incident.priority}</small><br>
            <small>Статус: ${incident.status}</small><br>
            <a href="/incidents/${incident.id}" class="btn btn-sm btn-primary mt-2">Детальніше</a>
        `);
    });
    
    // Додаємо легенду до карти
    addLegendToMap(map);
}

/**
 * Додавання легенди до карти
 */
function addLegendToMap(map) {
    const legend = L.control({position: 'bottomright'});
    
    legend.onAdd = function(map) {
        const div = L.DomUtil.create('div', 'info legend');
        div.innerHTML = `
            <h6>Пріоритет інцидентів</h6>
            <div><span style="display: inline-block; width: 12px; height: 12px; border-radius: 50%; background-color: #dc3545; margin-right: 5px;"></span> Високий</div>
            <div><span style="display: inline-block; width: 12px; height: 12px; border-radius: 50%; background-color: #ffc107; margin-right: 5px;"></span> Середній</div>
            <div><span style="display: inline-block; width: 12px; height: 12px; border-radius: 50%; background-color: #28a745; margin-right: 5px;"></span> Низький</div>
        `;
        return div;
    };
    
    legend.addTo(map);
}

/**
 * Оновлення списку інцидентів
 */
function updateIncidentsList(incidents) {
    const incidentsList = document.getElementById('incidents-list');
    if (!incidentsList) return;
    
    // Очищаємо список
    incidentsList.innerHTML = '';
    
    // Додаємо кожен інцидент до списку
    incidents.forEach(incident => {
        // Визначаємо клас для пріоритету
        let priorityClass;
        let priorityText;
        switch(incident.priority) {
            case 'high':
                priorityClass = 'text-danger';
                priorityText = 'Високий пріоритет';
                break;
            case 'medium':
                priorityClass = 'text-warning';
                priorityText = 'Середній пріоритет';
                break;
            case 'low':
                priorityClass = 'text-success';
                priorityText = 'Низький пріоритет';
                break;
            default:
                priorityClass = 'text-info';
                priorityText = 'Невизначений пріоритет';
        }
        
        // Форматуємо дату та час
        const date = new Date(incident.timestamp);
        const formattedDate = date.toLocaleDateString('uk-UA');
        const formattedTime = date.toLocaleTimeString('uk-UA', {hour: '2-digit', minute: '2-digit'});
        
        // Створюємо елемент для інциденту
        const incidentElement = document.createElement('div');
        incidentElement.className = 'incident-item mb-3';
        incidentElement.innerHTML = `
            <div class="d-flex justify-content-between">
                <h6 class="mb-1">${incident.title}</h6>
                <small class="text-muted">${formattedDate} ${formattedTime}</small>
            </div>
            <p class="mb-1">${incident.description}</p>
            <small class="${priorityClass}">${priorityText}</small>
            <div class="mt-2">
                <a href="/incidents/${incident.id}" class="btn btn-sm btn-outline-primary">Детальніше</a>
            </div>
        `;
        
        // Додаємо елемент до списку
        incidentsList.appendChild(incidentElement);
    });
}

/**
 * Ініціалізація фільтрів для інцидентів
 */
function initIncidentsFilter() {
    const filterForm = document.getElementById('incidents-filter-form');
    if (!filterForm) return;
    
    // Додаємо обробник події для форми фільтрів
    filterForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Отримуємо значення фільтрів
        const filters = {
            status: document.getElementById('filter-status').value,
            priority: document.getElementById('filter-priority').value,
            type: document.getElementById('filter-type').value,
            dateFrom: document.getElementById('filter-date-from').value,
            dateTo: document.getElementById('filter-date-to').value
        };
        
        // В реальній системі тут буде запит до API з фільтрами
        console.log('Застосовані фільтри:', filters);
        
        // Для демонстрації просто показуємо повідомлення
        alert('Фільтри застосовано. В реальній системі тут буде оновлений список інцидентів.');
    });
    
    // Додаємо обробник для кнопки скидання фільтрів
    const resetButton = document.getElementById('reset-filters');
    if (resetButton) {
        resetButton.addEventListener('click', function() {
            filterForm.reset();
        });
    }
}