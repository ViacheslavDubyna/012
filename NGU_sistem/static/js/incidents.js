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
    const incidents = [
        { id: 1, title: 'Спроба незаконного перетину кордону', lat: 50.1000, lng: 23.7000, type: 'порушення', severity: 'висока', status: 'активний' },
        { id: 2, title: 'Виявлення контрабанди', lat: 49.8500, lng: 23.1500, type: 'контрабанда', severity: 'середня', status: 'активний' },
        { id: 3, title: 'Порушення правил перетину кордону', lat: 48.4500, lng: 22.2200, type: 'порушення', severity: 'середня', status: 'активний' },
        { id: 4, title: 'Технічні проблеми на пункті пропуску', lat: 51.1500, lng: 23.8500, type: 'технічний', severity: 'низька', status: 'вирішений' },
        { id: 5, title: 'Затримання порушника', lat: 49.9000, lng: 24.0000, type: 'порушення', severity: 'висока', status: 'вирішений' }
    ];
    
    // Додаємо інциденти на карту
    const markers = [];
    incidents.forEach(incident => {
        // Визначаємо колір маркера залежно від статусу
        const markerColor = incident.status === 'активний' ? 'red' : 'gray';
        
        // Створюємо власний маркер з кольором
        const marker = L.circleMarker([incident.lat, incident.lng], {
            radius: 8,
            fillColor: markerColor,
            color: '#000',
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        }).addTo(map);
        
        // Додаємо спливаюче вікно з інформацією
        marker.bindPopup(`
            <strong>${incident.title}</strong><br>
            Тип: ${incident.type}<br>
            Рівень загрози: ${incident.severity}<br>
            Статус: ${incident.status}
        `);
        
        // Додаємо атрибути для фільтрації
        marker.incidentData = incident;
        markers.push(marker);
    });
    
    // Зберігаємо посилання на маркери для фільтрації
    window.incidentMarkers = {};
    markers.forEach((marker, index) => {
        window.incidentMarkers[index] = marker;
    });
    
    // Додаємо легенду до карти
    const legend = L.control({position: 'bottomright'});
    legend.onAdd = function(map) {
        const div = L.DomUtil.create('div', 'info legend');
        div.style.backgroundColor = 'white';
        div.style.padding = '10px';
        div.style.borderRadius = '5px';
        div.style.boxShadow = '0 0 15px rgba(0,0,0,0.2)';
        
        div.innerHTML = '<h6>Легенда</h6>' +
            '<div><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background-color:red;margin-right:5px;"></span> Активний інцидент</div>' +
            '<div><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background-color:gray;margin-right:5px;"></span> Вирішений інцидент</div>';
        
        return div;
    };
    legend.addTo(map);
}

/**
 * Ініціалізація фільтрів інцидентів
 */
function initIncidentsFilter() {
    const filterForm = document.querySelector('#priorityFilter')?.closest('form');
    if (!filterForm) return;
    
    // Додаємо обробник події для форми фільтрації
    filterForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Отримуємо значення фільтрів
        const priorityFilter = document.getElementById('priorityFilter').value;
        const dateFilter = document.getElementById('dateFilter').value;
        
        // Застосовуємо фільтри
        applyFilters(priorityFilter, dateFilter);
    });
}

/**
 * Застосування фільтрів до списку та карти інцидентів
 */
function applyFilters(priority, date) {
    // Фільтруємо маркери на карті
    if (window.incidentMarkers) {
        Object.values(window.incidentMarkers).forEach(marker => {
            if (marker.incidentData) {
                const incident = marker.incidentData;
                let visible = true;
                
                // Фільтр за пріоритетом
                if (priority !== 'all') {
                    const priorityMap = {
                        'high': 'висока',
                        'medium': 'середня',
                        'low': 'низька'
                    };
                    
                    if (incident.severity !== priorityMap[priority]) {
                        visible = false;
                    }
                }
                
                // Фільтр за датою (в демо-версії не реалізовано, оскільки немає дат у тестових даних)
                
                // Показуємо або приховуємо маркер
                if (visible) {
                    marker.setStyle({ opacity: 1, fillOpacity: 0.8 });
                } else {
                    marker.setStyle({ opacity: 0, fillOpacity: 0 });
                }
            }
        });}
    }
    
    // Фільтруємо список інцидентів
    const incidentItems = document.querySelectorAll('.list-group-item');
    incidentItems.forEach(item => {
        let visible = true;
        
        // Фільтр за пріоритетом
        if (priority !== 'all') {
            const priorityText = item.querySelector('small:last-child').textContent.toLowerCase();
            const priorityMap = {
                'high': 'високий пріоритет',
                'medium': 'середній пріоритет',
                'low': 'низький пріоритет'
            };
            
            if (!priorityText.includes(priorityMap[priority])) {
                visible = false;
            }
        }
        
        // Фільтр за датою (в демо-версії спрощено)
        if (date) {
            // В реальній системі тут буде порівняння дат
            // Для демо просто показуємо всі, якщо дата не вказана
        }
        
        // Показуємо або приховуємо елемент списку
        item.style.display = visible ? '' : 'none';
    });
