// Скрипт для візуалізації ресурсів з використанням Plotly.js

document.addEventListener('DOMContentLoaded', function() {
    // Перевіряємо наявність контейнера для графіка ресурсів
    if (document.getElementById('resource-indicators')) {
        initResourceIndicators();
    }
    
    // Перевіряємо наявність контейнерів для інших графіків ресурсів
    if (document.getElementById('resource-type-chart')) {
        initResourceTypeChart();
    }
    
    if (document.getElementById('resource-status-chart')) {
        initResourceStatusChart();
    }
});

/**
 * Ініціалізація індикаторів ресурсів з використанням Plotly.js
 */
function initResourceIndicators() {
    // Отримуємо дані про ресурси з API
    fetch('/api/resources/distribution')
        .then(response => response.json())
        .then(data => {
            createResourceIndicators(data);
        })
        .catch(error => {
            console.error('Помилка при отриманні даних про ресурси:', error);
            // Використовуємо тестові дані, якщо не вдалося отримати реальні
            createResourceIndicators(generateTestData());
        });
}

/**
 * Створення індикаторів ресурсів з використанням Plotly.js
 */
function createResourceIndicators(data) {
    // Підготовка даних для візуалізації
    const resources = [];
    const usages = [];
    
    // Перетворюємо дані у формат, необхідний для Plotly
    if (data.resources) {
        data.resources.forEach(resource => {
            resources.push(resource.name || resource.type);
            usages.push(resource.usage_percentage || resource.quantity_percentage);
        });
    } else if (data.by_type) {
        // Альтернативний формат даних
        Object.keys(data.by_type).forEach(type => {
            resources.push(type);
            usages.push(data.by_type[type].percentage);
        });
    }
    
    // Якщо даних немає, використовуємо тестові дані
    if (resources.length === 0) {
        const testData = generateTestData();
        resources.push(...testData.resources);
        usages.push(...testData.usages);
    }
    
    // Сортуємо ресурси за рівнем використання
    const sortedIndices = usages.map((usage, index) => ({ usage, index }))
        .sort((a, b) => b.usage - a.usage)
        .map(item => item.index);
    
    const sortedResources = sortedIndices.map(index => resources[index]);
    const sortedUsages = sortedIndices.map(index => usages[index]);
    
    // Створюємо контейнер для індикаторів
    const container = document.getElementById('resource-indicators');
    container.innerHTML = '';
    
    // Визначаємо кількість рядків і стовпців для сітки
    const numResources = sortedResources.length;
    const cols = 3;
    const rows = Math.ceil(numResources / cols);
    
    // Створюємо div для Plotly
    const plotDiv = document.createElement('div');
    plotDiv.id = 'resource-indicators-plot';
    plotDiv.style.width = '100%';
    plotDiv.style.height = `${rows * 150}px`;
    container.appendChild(plotDiv);
    
    // Створюємо індикатори з використанням Plotly
    const traces = [];
    
    for (let i = 0; i < numResources; i++) {
        const resource = sortedResources[i];
        const usage = sortedUsages[i];
        
        // Визначаємо колір індикатора залежно від рівня використання
        let color;
        if (usage > 80) {
            color = "#dc3545";  // Червоний (критичний)
        } else if (usage > 60) {
            color = "#fd7e14";  // Оранжевий (високий)
        } else {
            color = "#28a745";  // Зелений (нормальний)
        }
        
        // Розраховуємо позицію для індикатора в сітці
        const rowIdx = Math.floor(i / cols);
        const colIdx = i % cols;
        
        // Розраховуємо домен для індикатора
        const xDomain = [colIdx/cols, (colIdx+0.9)/cols];
        const yDomain = [1 - (rowIdx+1)/rows, 1 - rowIdx/rows];
        
        traces.push({
            type: 'indicator',
            mode: "gauge+number+delta",
            value: usage,
            domain: {'x': xDomain, 'y': yDomain},
            title: {
                text: resource,
                font: {size: 14, color: '#37474F'}
            },
            delta: {'reference': 50, 'increasing': {'color': "#dc3545"}, 'decreasing': {'color': "#28a745"}},
            gauge: {
                axis: {'range': [null, 100], 'tickwidth': 1, 'tickcolor': '#37474F'},
                bar: {'color': color},
                bgcolor: "white",
                borderwidth: 2,
                bordercolor: "gray",
                steps: [
                    {'range': [0, 60], 'color': 'rgba(40, 167, 69, 0.2)'},
                    {'range': [60, 80], 'color': 'rgba(253, 126, 20, 0.3)'},
                    {'range': [80, 100], 'color': 'rgba(220, 53, 69, 0.3)'}
                ],
                threshold: {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        });
    }
    
    // Створюємо макет
    const layout = {
        grid: {rows: rows, columns: cols, pattern: "independent"},
        margin: {l: 20, r: 20, t: 30, b: 20},
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        showlegend: false
    };
    
    // Відображаємо графік
    Plotly.newPlot('resource-indicators-plot', traces, layout, {responsive: true});
}

/**
 * Ініціалізація графіка розподілу ресурсів за типами
 */
function initResourceTypeChart() {
    fetch('/api/resources/distribution')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('resource-type-chart').getContext('2d');
            
            const labels = [];
            const values = [];
            const colors = [
                '#0057b7', '#1976D2', '#2196F3', '#64B5F6', '#90CAF9',
                '#ffd700', '#FFC107', '#FFEB3B', '#FFF59D', '#FFFDE7'
            ];
            
            if (data.by_type) {
                Object.keys(data.by_type).forEach((type, index) => {
                    labels.push(type);
                    values.push(data.by_type[type].count);
                });
            }
            
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                        backgroundColor: colors.slice(0, labels.length),
                        borderColor: '#FFFFFF',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'right',
                            labels: {
                                font: {
                                    size: 12
                                }
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.raw || 0;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = Math.round((value / total) * 100);
                                    return `${label}: ${value} (${percentage}%)`;
                                }
                            }
                        }
                    },
                    animation: {
                        animateScale: true,
                        animateRotate: true
                    }
                }
            });
        })
        .catch(error => {
            console.error('Помилка при отриманні даних про розподіл ресурсів:', error);
        });
}

/**
 * Ініціалізація графіка розподілу ресурсів за статусом
 */
function initResourceStatusChart() {
    fetch('/api/resources/distribution')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('resource-status-chart').getContext('2d');
            
            const labels = [];
            const values = [];
            const colors = {
                'Доступний': '#28a745',
                'Розгорнутий': '#0057b7',
                'На обслуговуванні': '#FFC107',
                'Резерв': '#6c757d',
                'Недоступний': '#dc3545'
            };
            const backgroundColors = [];
            
            if (data.by_status) {
                Object.keys(data.by_status).forEach(status => {
                    labels.push(status);
                    values.push(data.by_status[status].count);
                    backgroundColors.push(colors[status] || '#6c757d');
                });
            }
            
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Кількість ресурсів',
                        data: values,
                        backgroundColor: backgroundColors,
                        borderColor: backgroundColors.map(color => color.replace('0.7', '1')),
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: 'rgba(0, 0, 0, 0.1)'
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.dataset.label || '';
                                    const value = context.raw || 0;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = Math.round((value / total) * 100);
                                    return `${label}: ${value} (${percentage}%)`;
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Помилка при отриманні даних про розподіл ресурсів за статусом:', error);
        });
}

/**
 * Генерація тестових даних для візуалізації
 */
function generateTestData() {
    const resources = [
        'Військове обладнання', 'Гуманітарна допомога', 'Енергетичні ресурси',
        'Медичні засоби', 'Системи зв\'язку', 'Транспорт', 'Продовольство'
    ];
    
    const usages = resources.map(() => Math.floor(Math.random() * 50) + 50);
    
    return {
        resources: resources,
        usages: usages
    };
}