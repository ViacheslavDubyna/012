/**
 * Скрипт для відображення прогнозів перетину кордону
 * 
 * Цей файл містить функції для отримання та відображення графіків
 * прогнозів перетину кордону на наступний тиждень та місяць
 */

document.addEventListener('DOMContentLoaded', function() {
    // Перевіряємо, чи знаходимося ми на сторінці прогнозів
    if (document.querySelector('.chart-container')) {
        // Завантажуємо дані для тижневого прогнозу
        loadWeeklyPrediction();
        // Завантажуємо дані для місячного прогнозу
        loadMonthlyPrediction();
    }
});

/**
 * Завантаження даних тижневого прогнозу
 */
function loadWeeklyPrediction() {
    // В реальній системі дані будуть завантажуватися з API
    // Для демонстрації використовуємо тестові дані
    const data = {
        status: 'success',
        labels: ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд'],
        datasets: [
            {
                label: 'В'їзд',
                data: [1200, 1350, 1450, 1600, 1800, 2100, 1900],
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                fill: true
            },
            {
                label: 'Виїзд',
                data: [1100, 1250, 1350, 1500, 1700, 2000, 1800],
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                fill: true
            }
        ]
    };
    
    // Відображаємо графік тижневого прогнозу
    renderWeeklyPredictionChart(data);
}

/**
 * Завантаження даних місячного прогнозу
 */
function loadMonthlyPrediction() {
    // В реальній системі дані будуть завантажуватися з API
    // Для демонстрації використовуємо тестові дані
    const data = {
        status: 'success',
        labels: ['Тиждень 1', 'Тиждень 2', 'Тиждень 3', 'Тиждень 4'],
        datasets: [
            {
                label: 'В'їзд',
                data: [8500, 9200, 9800, 10500],
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                fill: true
            },
            {
                label: 'Виїзд',
                data: [8000, 8700, 9300, 10000],
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                fill: true
            }
        ]
    };
    
    // Відображаємо графік місячного прогнозу
    renderMonthlyPredictionChart(data);
}

/**
 * Відображення графіка тижневого прогнозу
 */
function renderWeeklyPredictionChart(data) {
    const ctx = document.getElementById('weekly-prediction-chart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: data.datasets
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Прогноз перетинів кордону на наступний тиждень'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                },
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Кількість осіб'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'День тижня'
                    }
                }
            }
        }
    });
}

/**
 * Відображення графіка місячного прогнозу
 */
function renderMonthlyPredictionChart(data) {
    const ctx = document.getElementById('monthly-prediction-chart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: data.datasets
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Прогноз перетинів кордону на наступний місяць'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                },
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Кількість осіб'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Тиждень'
                    }
                }
            }
        }
    });
}

/**
 * Функція для оновлення параметрів прогнозу
 */
function updatePredictionParams() {
    const form = document.getElementById('prediction-params-form');
    if (!form) return;
    
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Отримуємо значення параметрів
        const params = {
            checkpoint: document.getElementById('param-checkpoint').value,
            direction: document.getElementById('param-direction').value,
            period: document.getElementById('param-period').value
        };
        
        // В реальній системі тут буде запит до API з параметрами
        console.log('Параметри прогнозу:', params);
        
        // Для демонстрації просто показуємо повідомлення
        alert('Параметри прогнозу оновлено. В реальній системі тут будуть оновлені графіки.');
    });
}

// Ініціалізуємо форму параметрів прогнозу
document.addEventListener('DOMContentLoaded', function() {
    updatePredictionParams();
});