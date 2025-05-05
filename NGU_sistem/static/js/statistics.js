// Файл для роботи з графіками та таблицями на сторінці статистики

document.addEventListener('DOMContentLoaded', function() {
    // Ініціалізація графіків після завантаження DOM
    initIncidentsByTypeChart();
    initIncidentsByRegionChart();
    initIncidentsTimelineChart();

    // Додаємо обробник подій для кнопки фільтрів
    document.querySelector('.btn-primary').addEventListener('click', function() {
        // Оновлення графіків при зміні фільтрів
        updateCharts();
    });
});

// Графік кількості інцидентів за типом
function initIncidentsByTypeChart() {
    const ctx = document.getElementById('incidents-by-type-chart').getContext('2d');
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Порушення громадського порядку', 'Напад на патруль', 'Проникнення на охороняємий обєкт', 'Інші порушення'],
            datasets: [{
                data: [156, 98, 72, 48],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                },
                title: {
                    display: false
                }
            }
        }
    });
}

// Графік кількості інцидентів за областями
function initIncidentsByRegionChart() {
    const ctx = document.getElementById('incidents-by-region-chart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Львівська', 'Київська', 'Одеська', 'Харківська', 'Закарпатська'],
            datasets: [{
                label: 'Кількість інцидентів',
                data: [85, 64, 72, 53, 100],
                backgroundColor: 'rgba(54, 162, 235, 0.7)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Графік динаміки інцидентів за період
function initIncidentsTimelineChart() {
    const ctx = document.getElementById('incidents-timeline-chart').getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд'],
            datasets: [{
                label: 'Порушення кордону',
                data: [12, 19, 15, 17, 22, 24, 15],
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.1)',
                tension: 0.4,
                fill: true
            }, {
                label: 'Контрабанда',
                data: [8, 15, 12, 9, 14, 17, 13],
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Функція оновлення графіків при зміні фільтрів
function updateCharts() {
    // Тут буде код для оновлення даних графіків на основі вибраних фільтрів
    // В реальному додатку тут був би AJAX-запит до сервера для отримання нових даних
    console.log('Оновлення графіків з новими фільтрами');
    
    // Для демонстрації просто показуємо повідомлення
    alert('Фільтри застосовано. Графіки оновлено.');
}