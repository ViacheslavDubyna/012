/**
 * Головний JavaScript файл для інформаційно-аналітичної системи ДПСУ
 * 
 * Цей файл містить загальні функції, які використовуються на всіх сторінках системи
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Інформаційно-аналітична система ДПСУ завантажена');
    
    // Ініціалізація спільних компонентів інтерфейсу
    initCommonUI();
});

/**
 * Ініціалізація спільних компонентів інтерфейсу
 */
function initCommonUI() {
    // Активація підказок Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Активація випадаючих меню Bootstrap
    const dropdownTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="dropdown"]'));
    dropdownTriggerList.map(function (dropdownTriggerEl) {
        return new bootstrap.Dropdown(dropdownTriggerEl);
    });
    
    // Обробка кліків на елементах навігації
    setupNavigation();
}

/**
 * Налаштування навігації
 */
function setupNavigation() {
    // Підсвічування активного пункту меню
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href) && href !== '/') {
            link.classList.add('active');
        }
    });
    
    // Обробка кліків на кнопках фільтрів
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filterType = this.dataset.filter;
            console.log(`Застосовано фільтр: ${filterType}`);
            // Тут буде логіка фільтрації даних
        });
    });
}

/**
 * Форматування дати у локальному форматі
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('uk-UA', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}

/**
 * Форматування числа з розділювачами тисяч
 */
function formatNumber(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}

/**
 * Відображення повідомлення про помилку
 */
function showError(message) {
    const errorContainer = document.createElement('div');
    errorContainer.className = 'alert alert-danger alert-dismissible fade show';
    errorContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Додаємо повідомлення на сторінку
    const container = document.querySelector('.container');
    if (container) {
        container.prepend(errorContainer);
        
        // Автоматичне закриття через 5 секунд
        setTimeout(() => {
            const alert = bootstrap.Alert.getOrCreateInstance(errorContainer);
            alert.close();
        }, 5000);
    }
}