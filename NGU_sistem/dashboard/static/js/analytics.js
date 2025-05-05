/**
 * Скрипт для аналітичного дашборду НГУ
 * 
 * Цей файл містить функції для відображення аналітичних графіків та діаграм,
 * а також для роботи з фільтрами даних
 */

document.addEventListener('DOMContentLoaded', function() {
    // Ініціалізуємо графіки
    initAnalyticsCharts();
    
    // Ініціалізуємо фільтри
    initAnalyticsFilters();
});

/**
 * Ініціалізація аналітичних графіків
 */
function initAnalyticsCharts() {
    // Графік тенденцій інцидентів
    const trendsCtx = document.getElementById('incidentsTrendsChart');
    if (trendsCtx) {
        new Chart(trendsCtx, {
            type: 'line',
            data: {
                labels: ['Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень'],
                datasets: [{
                    label: 'Порушення громадського порядку',
                    data: [65, 59, 80, 81, 56, 55],
                    borderColor: '#1b3a1b',
                    backgroundColor: 'rgba(27, 58, 27, 0.1)',
                    tension: 0.3
                }, {
                    label: 'Масові заходи',
                    data: [28, 48, 40, 19, 86, 27],
                    borderColor: '#FFD700',
                    backgroundColor: 'rgba(255, 215, 0, 0.1)',
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Тенденції інцидентів за останні 6 місяців'
                    }
                }
            }
        });
    }

    // Графік розподілу інцидентів за типами
    const typesCtx = document.getElementById('incidentsTypesChart');
    if (typesCtx) {
        new Chart(typesCtx, {
            type: 'doughnut',
            data: {
                labels: [
                    'Порушення громадського порядку',
                    'Масові заходи',
                    'Кримінальні правопорушення',
                    'Надзвичайні ситуації',
                    'Інше'
                ],
                datasets: [{
                    data: [35, 25, 20, 15, 5],
                    backgroundColor: [
                        '#1b3a1b',
                        '#2c5e2c',
                        '#FFD700',
                        '#d4af37',
                        '#808080'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right',
                    },
                    title: {
                        display: true,
                        text: 'Розподіл інцидентів за типами'
                    }
                }
            }
        });
    }

    // Графік розподілу інцидентів за регіонами
    const regionsCtx = document.getElementById('incidentsRegionsChart');
    if (regionsCtx) {
        new Chart(regionsCtx, {
            type: 'bar',
            data: {
                labels: ['Київ', 'Харків', 'Одеса', 'Львів', 'Дніпро', 'Запоріжжя', 'Донецьк', 'Луганськ'],
                datasets: [{
                    label: 'Кількість інцидентів',
                    data: [120, 90, 85, 70, 65, 60, 55, 50],
                    backgroundColor: '#1b3a1b'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Розподіл інцидентів за регіонами'
                    }
                }
            }
        });
    }
}

/**
 * Ініціалізація фільтрів для аналітики
 */
function initAnalyticsFilters() {
    // Обробка зміни періоду
    const periodFilter = document.getElementById('periodFilter');
    if (periodFilter) {
        periodFilter.addEventListener('change', function() {
            // Тут буде логіка оновлення даних при зміні періоду
            console.log('Період змінено на: ' + this.value);
            // updateAnalyticsData(this.value);
        });
    }

    // Обробка зміни типу інцидентів
    const typeFilter = document.getElementById('typeFilter');
    if (typeFilter) {
        typeFilter.addEventListener('change', function() {
            // Тут буде логіка оновлення даних при зміні типу інцидентів
            console.log('Тип інцидентів змінено на: ' + this.value);
            // updateAnalyticsData(null, this.value);
        });
    }

    // Обробка зміни регіону
    const regionFilter = document.getElementById('regionFilter');
    if (regionFilter) {
        regionFilter.addEventListener('change', function() {
            // Тут буде логіка оновлення даних при зміні регіону
            console.log('Регіон змінено на: ' + this.value);
            // updateAnalyticsData(null, null, this.value);
        });
    }
}

/**
 * Оновлення аналітичних даних на основі фільтрів
 */
function updateAnalyticsData(period, type, region) {
    // Тут буде логіка запиту до API та оновлення графіків
    console.log('Оновлення даних з параметрами:', { period, type, region });
    
    // Приклад запиту до API
    // fetch(`/api/analytics?period=${period}&type=${type}&region=${region}`)
    //     .then(response => response.json())
    //     .then(data => {
    //         // Оновлення графіків з новими даними
    //         updateCharts(data);
    //     })
    //     .catch(error => console.error('Помилка при отриманні даних:', error));
}