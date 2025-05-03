// JavaScript для сторінки аналітики ДПСУ

document.addEventListener('DOMContentLoaded', function() {
    // Перевіряємо, чи є на сторінці контейнер для графіка аналізу тенденцій
    const trendChartContainer = document.querySelector('.chart-container');
    if (trendChartContainer) {
        initTrendChart();
    }
});

// Функція ініціалізації графіка аналізу тенденцій
async function initTrendChart() {
    try {
        // Отримуємо дані з API
        const response = await fetch('/api/border_crossing_trends');
        if (!response.ok) {
            throw new Error('Не вдалося отримати дані про тенденції перетину кордону');
        }
        
        const data = await response.json();
        
        // Видаляємо заглушку
        const chartContainer = document.querySelector('.chart-container');
        chartContainer.innerHTML = '<canvas id="trendChart"></canvas>';
        
        // Отримуємо контекст для графіка
        const ctx = document.getElementById('trendChart').getContext('2d');
        
        // Створюємо графік за допомогою Chart.js
        new Chart(ctx, {
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
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Тенденції перетину кордону за останні 30 днів',
                        font: {
                            size: 16
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    },
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Дата'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Кількість'
                        },
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (error) {
        console.error('Помилка при ініціалізації графіка:', error);
        const chartContainer = document.querySelector('.chart-container');
        chartContainer.innerHTML = `<div class="alert alert-danger">Помилка при завантаженні даних: ${error.message}</div>`;
    }
}