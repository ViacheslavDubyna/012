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
    fetch('/api/border_crossing_weekly_prediction')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Відображаємо графік тижневого прогнозу
                renderWeeklyPredictionChart(data);
            } else {
                console.error('Помилка отримання даних тижневого прогнозу');
            }
        })
        .catch(error => {
            console.error('Помилка завантаження даних тижневого прогнозу:', error);
        });
}

/**
 * Завантаження даних місячного прогнозу
 */
function loadMonthlyPrediction() {
    fetch('/api/border_crossing_monthly_prediction')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Відображаємо графік місячного прогнозу
                renderMonthlyPredictionChart(data);
            } else {
                console.error('Помилка отримання даних місячного прогнозу');
            }
        })
        .catch(error => {
            console.error('Помилка завантаження даних місячного прогнозу:', error);
        });
}

/**
 * Відображення графіка тижневого прогнозу
 */
function renderWeeklyPredictionChart(data) {
    // Знаходимо контейнер для графіка короткострокового прогнозу
    const weeklyChartContainer = Array.from(document.querySelectorAll('.card-title'))
        .find(el => el.textContent.includes('Короткостроковий прогноз'))
        .closest('.card')
        .querySelector('.chart-container');
    
    // Очищаємо контейнер від тексту-заповнювача
    weeklyChartContainer.innerHTML = '';
    
    // Створюємо елемент canvas для графіка
    const canvas = document.createElement('canvas');
    canvas.id = 'weeklyPredictionChart';
    weeklyChartContainer.appendChild(canvas);
    
    // Створюємо графік за допомогою Chart.js
    new Chart(canvas, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [
                {
                    label: 'Громадяни України',
                    data: data.ukrainian_citizens,
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Іноземні громадяни',
                    data: data.foreign_citizens,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Транспортні засоби',
                    data: data.vehicles,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.4,
                    fill: true
                }
            ]
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
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Кількість перетинів'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Дата'
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
    // Знаходимо контейнер для графіка довгострокового прогнозу
    const monthlyChartContainer = Array.from(document.querySelectorAll('.card-title'))
        .find(el => el.textContent.includes('Довгостроковий прогноз'))
        .closest('.card')
        .querySelector('.chart-container');
    
    // Очищаємо контейнер від тексту-заповнювача
    monthlyChartContainer.innerHTML = '';
    
    // Створюємо елемент canvas для графіка
    const canvas = document.createElement('canvas');
    canvas.id = 'monthlyPredictionChart';
    monthlyChartContainer.appendChild(canvas);
    
    // Створюємо графік за допомогою Chart.js
    new Chart(canvas, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [
                {
                    label: 'Громадяни України',
                    data: data.ukrainian_citizens,
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Іноземні громадяни',
                    data: data.foreign_citizens,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Транспортні засоби',
                    data: data.vehicles,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.4,
                    fill: true
                }
            ]
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
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Кількість перетинів'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Дата'
                    }
                }
            }
        }
    });
}