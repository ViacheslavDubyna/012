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
    initFilters();
    
    // Ініціалізуємо кнопки дій
    initActionButtons();
});

/**
 * Ініціалізація карти інцидентів
 */
function initIncidentsMap() {
    // Перевіряємо, чи існує контейнер для карти
    const mapContainer = document.getElementById('incidents-map');
    if (!mapContainer) return;
    
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
            id: 'INC-2025-0142',
            title: 'Порушення громадського порядку',
            description: 'Масове порушення громадського порядку під час проведення мітингу.',
            priority: 'medium',
            status: 'active',
            location: {
                lat: 50.4501,
                lng: 30.5234
            },
            address: 'Київ, вул. Хрещатик',
            timestamp: '2025-05-12T08:45:00'
        },
        {
            id: 'INC-2025-0141',
            title: 'Масовий захід',
            description: 'Забезпечення охорони громадського порядку під час проведення масового заходу.',
            priority: 'high',
            status: 'in-progress',
            location: {
                lat: 49.8397,
                lng: 24.0297
            },
            address: 'Львів, площа Ринок',
            timestamp: '2025-05-12T07:30:00'
        },
        {
            id: 'INC-2025-0140',
            title: 'Охорона об\'єкту',
            description: 'Посилення охорони стратегічного об\'єкту у зв\'язку з підвищеним рівнем загрози.',
            priority: 'medium',
            status: 'in-progress',
            location: {
                lat: 49.9935,
                lng: 36.2304
            },
            address: 'Харків, вул. Сумська',
            timestamp: '2025-05-11T23:15:00'
        },
        {
            id: 'INC-2025-0139',
            title: 'Транспортування цінностей',
            description: 'Забезпечення безпеки під час транспортування цінних вантажів.',
            priority: 'medium',
            status: 'resolved',
            location: {
                lat: 46.4825,
                lng: 30.7233
            },
            address: 'Одеса, вул. Дерибасівська',
            timestamp: '2025-05-11T18:20:00'
        },
        {
            id: 'INC-2025-0138',
            title: 'Порушення громадського порядку',
            description: 'Локальне порушення громадського порядку групою осіб.',
            priority: 'low',
            status: 'resolved',
            location: {
                lat: 48.4647,
                lng: 35.0462
            },
            address: 'Дніпро, просп. Яворницького',
            timestamp: '2025-05-11T14:10:00'
        }
    ];
    
    // Додаємо маркери на карту
    addIncidentsToMap(map, testData);
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
        
        // Створюємо іконку для маркера
        const icon = L.divIcon({
            html: `<div style="width: 12px; height: 12px; border-radius: 50%; background-color: ${markerColor};"></div>`,
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
            <p><strong>Місце:</strong> ${incident.address}</p>
            <p><strong>Пріоритет:</strong> ${getPriorityText(incident.priority)}</p>
            <p><strong>Статус:</strong> ${getStatusText(incident.status)}</p>
            <button class="btn btn-sm btn-primary mt-2" onclick="showIncidentDetails('${incident.id}')">Детальніше</button>
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
        div.style.backgroundColor = 'white';
        div.style.padding = '10px';
        div.style.borderRadius = '5px';
        div.style.boxShadow = '0 0 10px rgba(0,0,0,0.1)';
        
        div.innerHTML = `
            <h6 class="mb-2">Пріоритет інцидентів</h6>
            <div class="mb-1"><span style="display: inline-block; width: 12px; height: 12px; border-radius: 50%; background-color: #dc3545; margin-right: 5px;"></span> Високий</div>
            <div class="mb-1"><span style="display: inline-block; width: 12px; height: 12px; border-radius: 50%; background-color: #ffc107; margin-right: 5px;"></span> Середній</div>
            <div><span style="display: inline-block; width: 12px; height: 12px; border-radius: 50%; background-color: #28a745; margin-right: 5px;"></span> Низький</div>
        `;
        return div;
    };
    
    legend.addTo(map);
}

/**
 * Ініціалізація фільтрів
 */
function initFilters() {
    const filterButton = document.querySelector('button.btn-primary');
    if (!filterButton) return;
    
    filterButton.addEventListener('click', function() {
        const status = document.getElementById('incident-status').value;
        const type = document.getElementById('incident-type').value;
        const region = document.getElementById('incident-region').value;
        
        // В реальній системі тут буде запит до API з фільтрами
        console.log('Застосовані фільтри:', { status, type, region });
        
        // Для демонстрації просто показуємо повідомлення
        alert(`Фільтри застосовано: Статус - ${status}, Тип - ${type}, Регіон - ${region}`);
    });
}

/**
 * Ініціалізація кнопок дій
 */
function initActionButtons() {
    // Кнопка "Додати інцидент"
    const addButton = document.querySelector('button.btn-outline-primary');
    if (addButton) {
        addButton.addEventListener('click', function() {
            alert('Відкриття форми для додавання нового інциденту');
        });
    }
    
    // Кнопка "Експорт"
    const exportButton = document.querySelector('button.btn-outline-secondary');
    if (exportButton) {
        exportButton.addEventListener('click', function() {
            alert('Експорт списку інцидентів');
        });
    }
    
    // Кнопки "Деталі"
    const detailButtons = document.querySelectorAll('button.btn-outline-primary');
    detailButtons.forEach(button => {
        button.addEventListener('click', function() {
            const row = this.closest('tr');
            const id = row.cells[0].textContent;
            showIncidentDetails(id);
        });
    });
    
    // Кнопки швидких дій
    const quickActionButtons = document.querySelectorAll('.card .btn-outline-danger, .card .btn-outline-warning, .card .btn-outline-info');
    quickActionButtons.forEach(button => {
        button.addEventListener('click', function() {
            alert(`Дія: ${this.textContent}`);
        });
    });
}

/**
 * Показати деталі інциденту
 */
function showIncidentDetails(id) {
    alert(`Відкриття деталей інциденту з ID: ${id}`);
}

/**
 * Отримати текстовий опис пріоритету
 */
function getPriorityText(priority) {
    switch(priority) {
        case 'high': return 'Високий';
        case 'medium': return 'Середній';
        case 'low': return 'Низький';
        default: return 'Невизначений';
    }
}

/**
 * Отримати текстовий опис статусу
 */
function getStatusText(status) {
    switch(status) {
        case 'active': return 'Активний';
        case 'in-progress': return 'В обробці';
        case 'resolved': return 'Вирішений';
        case 'archived': return 'Архівований';
        default: return 'Невизначений';
    }
}