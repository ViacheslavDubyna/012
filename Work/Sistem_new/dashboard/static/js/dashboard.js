/**
 * JavaScript для системи підтримки прийняття рішень ГУ НГУ
 */

// Глобальні змінні для графіків
let locationCasualtiesChart;
let timeCasualtiesChart;
let unitCasualtiesChart;
let incidentTypesChart;

// Ініціалізація при завантаженні сторінки
document.addEventListener('DOMContentLoaded', function() {
    // Завантаження даних з API
    fetchAnalyticsData();
    
    // Налаштування форми моделювання сценаріїв
    setupScenarioForm();
    
    // Оновлення значення інтенсивності
    const intensitySlider = document.getElementById('intensity');
    const intensityValue = document.getElementById('intensity-value');
    
    if (intensitySlider && intensityValue) {
        intensitySlider.addEventListener('input', function() {
            intensityValue.textContent = this.value;
        });
    }
});

/**
 * Завантаження аналітичних даних з API
 */
function fetchAnalyticsData() {
    fetch('/api/analytics')
        .then(response => {
            if (!response.ok) {
                throw new Error('Помилка завантаження даних');
            }
            return response.json();
        })
        .then(data => {
            // Відображення даних на дашборді
            displayOperationalData(data.data);
            displayCasualtiesByLocation(data.location_stats);
            displayCasualtiesByTime(data.time_stats);
            displayIncidentTypes(data.type_stats);
            displayUnitCasualties(data.unit_stats);
            displayThreatPredictions(data);
            displayDecisionsLog(data);
            displayRecommendedActions(data);
        })
        .catch(error => {
            console.error('Помилка:', error);
            alert('Не вдалося завантажити дані. Спробуйте оновити сторінку.');
        });
}

/**
 * Відображення оперативних даних
 */
function displayOperationalData(data) {
    if (!data || !data.operational_data) return;
    
    const tableBody = document.getElementById('operational-data');
    if (!tableBody) return;
    
    tableBody.innerHTML = '';
    
    // Сортування за рівнем загрози (спадання)
    const sortedData = [...data.operational_data].sort((a, b) => b.threat_level - a.threat_level);
    
    sortedData.forEach(item => {
        const row = document.createElement('tr');
        
        // Додавання класу залежно від рівня загрози
        row.classList.add(`threat-level-${item.threat_level}`);
        
        row.innerHTML = `
            <td>${item.location}</td>
            <td>${item.description}</td>
            <td>${item.threat_level}</td>
            <td>${new Date(item.timestamp).toLocaleString('uk-UA')}</td>
        `;
        
        tableBody.appendChild(row);
    });
}

/**
 * Відображення втрат за локаціями
 */
function displayCasualtiesByLocation(data) {
    if (!data) return;
    
    const ctx = document.getElementById('location-casualties-chart');
    if (!ctx) return;
    
    // Знищення попереднього графіка, якщо він існує
    if (locationCasualtiesChart) {
        locationCasualtiesChart.destroy();
    }
    
    // Підготовка даних для графіка
    const locations = data.map(item => item.location);
    const casualties = data.map(item => item.casualties);
    const wounded = data.map(item => item.wounded);
    
    // Створення графіка
    locationCasualtiesChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: locations,
            datasets: [
                {
                    label: 'Безповоротні втрати',
                    data: casualties,
                    backgroundColor: 'rgba(220, 53, 69, 0.8)',
                    borderColor: 'rgba(220, 53, 69, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Санітарні втрати',
                    data: wounded,
                    backgroundColor: 'rgba(255, 193, 7, 0.8)',
                    borderColor: 'rgba(255, 193, 7, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Кількість'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Локація'
                    }
                }
            }
        }
    });
}

/**
 * Відображення втрат за часом
 */
function displayCasualtiesByTime(data) {
    if (!data) return;
    
    const ctx = document.getElementById('time-casualties-chart');
    if (!ctx) return;
    
    // Знищення попереднього графіка, якщо він існує
    if (timeCasualtiesChart) {
        timeCasualtiesChart.destroy();
    }
    
    // Підготовка даних для графіка
    const dates = data.map(item => item.date);
    const casualties = data.map(item => item.casualties);
    const wounded = data.map(item => item.wounded);
    
    // Створення графіка
    timeCasualtiesChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Безповоротні втрати',
                    data: casualties,
                    backgroundColor: 'rgba(220, 53, 69, 0.2)',
                    borderColor: 'rgba(220, 53, 69, 1)',
                    borderWidth: 2,
                    tension: 0.1
                },
                {
                    label: 'Санітарні втрати',
                    data: wounded,
                    backgroundColor: 'rgba(255, 193, 7, 0.2)',
                    borderColor: 'rgba(255, 193, 7, 1)',
                    borderWidth: 2,
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Кількість'
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
 * Відображення типів інцидентів
 */
function displayIncidentTypes(data) {
    if (!data) return;
    
    const ctx = document.getElementById('incident-types-chart');
    if (!ctx) return;
    
    // Знищення попереднього графіка, якщо він існує
    if (incidentTypesChart) {
        incidentTypesChart.destroy();
    }
    
    // Підготовка даних для графіка
    const types = data.map(item => item.incident_type);
    const counts = data.map(item => item.count);
    const casualties = data.map(item => item.casualties);
    
    // Створення графіка
    incidentTypesChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: types,
            datasets: [
                {
                    data: counts,
                    backgroundColor: [
                        'rgba(220, 53, 69, 0.8)',
                        'rgba(255, 193, 7, 0.8)',
                        'rgba(40, 167, 69, 0.8)',
                        'rgba(0, 123, 255, 0.8)',
                        'rgba(111, 66, 193, 0.8)'
                    ],
                    borderColor: [
                        'rgba(220, 53, 69, 1)',
                        'rgba(255, 193, 7, 1)',
                        'rgba(40, 167, 69, 1)',
                        'rgba(0, 123, 255, 1)',
                        'rgba(111, 66, 193, 1)'
                    ],
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const casualty = casualties[context.dataIndex] || 0;
                            return `${label}: ${value} інцидентів, ${casualty} втрат`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Відображення втрат за підрозділами
 */
function displayUnitCasualties(data) {
    if (!data) return;
    
    const ctx = document.getElementById('unit-casualties-chart');
    if (!ctx) return;
    
    // Знищення попереднього графіка, якщо він існує
    if (unitCasualtiesChart) {
        unitCasualtiesChart.destroy();
    }
    
    // Підготовка даних для графіка
    const units = data.map(item => item.unit);
    const casualties = data.map(item => item.casualties);
    const wounded = data.map(item => item.wounded);
    
    // Створення графіка
    unitCasualtiesChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: units,
            datasets: [
                {
                    label: 'Безповоротні втрати',
                    data: casualties,
                    backgroundColor: 'rgba(220, 53, 69, 0.8)',
                    borderColor: 'rgba(220, 53, 69, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Санітарні втрати',
                    data: wounded,
                    backgroundColor: 'rgba(255, 193, 7, 0.8)',
                    borderColor: 'rgba(255, 193, 7, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Кількість'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Підрозділ'
                    }
                }
            }
        }
    });
}

/**
 * Відображення прогнозів загроз
 */
function displayThreatPredictions(data) {
    if (!data || !data.predictions) return;
    
    const tableBody = document.getElementById('threat-predictions');
    if (!tableBody) return;
    
    tableBody.innerHTML = '';
    
    // Сортування за ймовірністю (спадання)
    const sortedData = [...data.predictions].sort((a, b) => b.probability - a.probability);
    
    sortedData.forEach(item => {
        const row = document.createElement('tr');
        
        // Додавання класу залежно від ймовірності
        if (item.probability >= 70) {
            row.classList.add('table-danger');
        } else if (item.probability >= 40) {
            row.classList.add('table-warning');
        } else {
            row.classList.add('table-success');
        }
        
        row.innerHTML = `
            <td>${item.location}</td>
            <td>${item.threat_type}</td>
            <td>${item.probability.toFixed(1)}</td>
            <td>${item.expected_casualties}</td>
        `;
        
        tableBody.appendChild(row);
    });
}

/**
 * Відображення журналу рішень
 */
function displayDecisionsLog(data) {
    if (!data || !data.decisions) return;
    
    const tableBody = document.getElementById('decisions-log');
    if (!tableBody) return;
    
    tableBody.innerHTML = '';
    
    // Сортування за часом (спадання)
    const sortedData = [...data.decisions].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    
    sortedData.forEach(item => {
        const row = document.createElement('tr');
        
        // Додавання класу залежно від ефективності
        if (item.effectiveness >= 8) {
            row.classList.add('table-success');
        } else if (item.effectiveness >= 5) {
            row.classList.add('table-warning');
        } else {
            row.classList.add('table-danger');
        }
        
        row.innerHTML = `
            <td>${new Date(item.timestamp).toLocaleString('uk-UA')}</td>
            <td>${item.description}</td>
            <td>${item.action_taken}</td>
            <td>${item.result || 'Немає даних'}</td>
            <td>${item.effectiveness}/10</td>
        `;
        
        tableBody.appendChild(row);
    });
}

/**
 * Відображення рекомендованих дій
 */
function displayRecommendedActions(data) {
    if (!data || !data.recommendations) return;
    
    const actionsContainer = document.getElementById('recommended-actions');
    if (!actionsContainer) return;
    
    actionsContainer.innerHTML = '';
    
    // Сортування за пріоритетом (спадання)
    const sortedData = [...data.recommendations].sort((a, b) => b.priority - a.priority);
    
    sortedData.forEach(item => {
        const actionItem = document.createElement('div');
        actionItem.className = 'list-group-item';
        
        // Додавання класу залежно від пріоритету
        if (item.priority >= 8) {
            actionItem.classList.add('high-priority');
        } else if (item.priority >= 5) {
            actionItem.classList.add('medium-priority');
        } else {
            actionItem.classList.add('low-priority');
        }
        
        actionItem.innerHTML = `
            <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-1">${item.title}</h5>
                <small>Пріоритет: ${item.priority}/10</small>
            </div>
            <p class="mb-1">${item.description}</p>
            <small>Очікувана ефективність: ${item.expected_effectiveness}/10</small>
        `;
        
        actionsContainer.appendChild(actionItem);
    });
}

/**
 * Налаштування форми моделювання сценаріїв
 */
function setupScenarioForm() {
    const form = document.getElementById('scenario-form');
    if (!form) return;
    
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Отримання значень з форми
        const location = document.getElementById('location').value;
        const threatType = document.getElementById('threat-type').value;
        const intensity = document.getElementById('intensity').value;
        
        // Відправка запиту на сервер
        fetch('/api/simulate-scenario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                location: location,
                threat_type: threatType,
                intensity: parseInt(intensity)
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Помилка моделювання сценарію');
            }
            return response.json();
        })
        .then(data => {
            displayScenarioResult(data);
        })
        .catch(error => {
            console.error('Помилка:', error);
            alert('Не вдалося змоделювати сценарій. Спробуйте ще раз.');
        });
    });
}

/**
 * Відображення результатів моделювання сценарію
 */
function displayScenarioResult(data) {
    const resultContainer = document.getElementById('scenario-result');
    if (!resultContainer) return;
    
    resultContainer.innerHTML = `
        <div class="alert ${data.risk_level >= 7 ? 'alert-danger' : data.risk_level >= 4 ? 'alert-warning' : 'alert-success'}">
            <h4>Результати моделювання</h4>
            <p><strong>Рівень ризику:</strong> ${data.risk_level}/10</p>
            <p><strong>Очікувані втрати:</strong> ${data.expected_casualties} безповоротних, ${data.expected_wounded} санітарних</p>
            <p><strong>Рекомендації:</strong> ${data.recommendations}</p>
        </div>
    `;
}