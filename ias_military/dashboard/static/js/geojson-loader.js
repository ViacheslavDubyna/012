/**
 * Модуль для безпечного завантаження GeoJSON даних України
 * з обробкою помилок та резервними джерелами
 */

// Основне джерело GeoJSON даних України
const PRIMARY_GEOJSON_URL = 'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/ukraine.geojson';

// Резервне джерело GeoJSON даних України
const BACKUP_GEOJSON_URL = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries/UKR.geo.json';

// Локальний шлях до GeoJSON файлу (якщо є)
const LOCAL_GEOJSON_PATH = '/static/data/ukraine.geojson';

/**
 * Функція для безпечного завантаження GeoJSON даних України
 * @param {Function} successCallback - Функція, яка викликається при успішному завантаженні даних
 * @param {Function} errorCallback - Функція, яка викликається при помилці завантаження
 */
function loadUkraineGeoJSON(successCallback, errorCallback) {
    // Спробуємо завантажити з основного джерела
    fetch(PRIMARY_GEOJSON_URL)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Помилка завантаження GeoJSON: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('GeoJSON успішно завантажено з основного джерела');
            successCallback(data);
        })
        .catch(error => {
            console.warn(`Помилка завантаження GeoJSON з основного джерела: ${error.message}. Спроба використати резервне джерело...`);
            
            // Спробуємо завантажити з резервного джерела
            fetch(BACKUP_GEOJSON_URL)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Помилка завантаження GeoJSON: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('GeoJSON успішно завантажено з резервного джерела');
                    successCallback(data);
                })
                .catch(backupError => {
                    console.warn(`Помилка завантаження GeoJSON з резервного джерела: ${backupError.message}. Спроба використати локальний файл...`);
                    
                    // Спробуємо завантажити з локального файлу
                    fetch(LOCAL_GEOJSON_PATH)
                        .then(response => {
                            if (!response.ok) {
                                throw new Error(`Помилка завантаження GeoJSON: ${response.status}`);
                            }
                            return response.json();
                        })
                        .then(data => {
                            console.log('GeoJSON успішно завантажено з локального файлу');
                            successCallback(data);
                        })
                        .catch(localError => {
                            console.error(`Всі спроби завантаження GeoJSON зазнали невдачі: ${localError.message}`);
                            
                            // Викликаємо функцію обробки помилки
                            if (typeof errorCallback === 'function') {
                                errorCallback(localError);
                            }
                        });
                });
        });
}

/**
 * Функція для перевірки наявності локального файлу GeoJSON
 * @returns {Promise<boolean>} - Promise, який повертає true, якщо файл існує, і false в іншому випадку
 */
function checkLocalGeoJSONFile() {
    return new Promise((resolve) => {
        fetch(LOCAL_GEOJSON_PATH, { method: 'HEAD' })
            .then(response => {
                resolve(response.ok);
            })
            .catch(() => {
                resolve(false);
            });
    });
}

// Експортуємо функції для використання в інших модулях
window.GeoJSONLoader = {
    loadUkraineGeoJSON,
    checkLocalGeoJSONFile
};