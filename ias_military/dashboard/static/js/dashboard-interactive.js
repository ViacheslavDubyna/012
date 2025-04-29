та// Інтерактивні функції для дашборду

document.addEventListener('DOMContentLoaded', function() {
    // Ініціалізація тултіпів
    initTooltips();
    
    // Анімація для карток при прокрутці
    initScrollAnimations();
    
    // Додавання інтерактивності до кнопок
    initButtonEffects();
    
    // Покращення відображення карти
    enhanceMap();
});

/**
 * Ініціалізація тултіпів для інформаційних іконок
 */
function initTooltips() {
    // Додаємо обробники подій для всіх інформаційних іконок
    const infoIcons = document.querySelectorAll('.info-icon, [data-tooltip]');
    
    infoIcons.forEach(icon => {
        // Додаємо клас для стилізації курсора
        icon.classList.add('cursor-help');
        
        // Додаємо обробники подій для показу/приховування тултіпа
        icon.addEventListener('mouseenter', showTooltip);
        icon.addEventListener('mouseleave', hideTooltip);
    });
}

/**
 * Показ тултіпа
 */
function showTooltip(event) {
    const tooltipText = this.getAttribute('data-tooltip') || this.getAttribute('title');
    
    if (!tooltipText) return;
    
    // Створюємо елемент тултіпа
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip-popup animate__animated animate__fadeIn';
    tooltip.textContent = tooltipText;
    
    // Додаємо тултіп до документа
    document.body.appendChild(tooltip);
    
    // Позиціонуємо тултіп відносно елемента
    const rect = this.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
    
    // Зберігаємо посилання на тултіп
    this._tooltip = tooltip;
}

/**
 * Приховування тултіпа
 */
function hideTooltip() {
    if (this._tooltip) {
        this._tooltip.classList.replace('animate__fadeIn', 'animate__fadeOut');
        
        // Видаляємо тултіп після завершення анімації
        setTimeout(() => {
            if (this._tooltip && this._tooltip.parentNode) {
                this._tooltip.parentNode.removeChild(this._tooltip);
                this._tooltip = null;
            }
        }, 300);
    }
}

/**
 * Ініціалізація анімацій при прокрутці
 */
function initScrollAnimations() {
    // Отримуємо всі елементи, які потрібно анімувати
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    // Функція для перевірки, чи елемент видимий у вікні перегляду
    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.bottom >= 0
        );
    }
    
    // Функція для анімації елементів при прокрутці
    function animateOnScroll() {
        animatedElements.forEach(element => {
            if (isElementInViewport(element) && !element.classList.contains('animated')) {
                // Додаємо клас для анімації
                element.classList.add('animated', 'animate__fadeInUp');
            }
        });
    }
    
    // Додаємо обробник події прокрутки
    window.addEventListener('scroll', animateOnScroll);
    
    // Запускаємо анімацію при завантаженні сторінки
    animateOnScroll();
}

/**
 * Додавання ефектів до кнопок
 */
function initButtonEffects() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.classList.add('pulse');
        });
        
        button.addEventListener('mouseleave', function() {
            this.classList.remove('pulse');
        });
        
        button.addEventListener('click', function() {
            // Додаємо ефект хвилі при кліку
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            this.appendChild(ripple);
            
            // Видаляємо ефект після анімації
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

/**
 * Покращення відображення карти
 */
function enhanceMap() {
    // Перевіряємо наявність карти на сторінці
    const mapElement = document.getElementById('operational-map');
    if (!mapElement) return;
    
    // Додаємо легенду до карти
    const mapLegend = document.createElement('div');
    mapLegend.className = 'map-legend';
    mapLegend.innerHTML = `
        <div class="map-legend-title">Легенда</div>
        <div class="map-legend-item">
            <span class="map-legend-color" style="background-color: #28a745;"></span>
            <span>Штатна ситуація</span>
        </div>
        <div class="map-legend-item">
            <span class="map-legend-color" style="background-color: #ffc107;"></span>
            <span>Напружена ситуація</span>
        </div>
        <div class="map-legend-item">
            <span class="map-legend-color" style="background-color: #dc3545;"></span>
            <span>Критична ситуація</span>
        </div>
        <div class="map-legend-item">
            <span class="map-legend-color" style="background-color: #0057b7;"></span>
            <span>Підрозділи НГУ</span>
        </div>
    `;
    
    // Додаємо легенду до контейнера карти
    mapElement.parentNode.appendChild(mapLegend);
    
    // Додаємо інформаційну панель
    const mapInfo = document.createElement('div');
    mapInfo.className = 'map-overlay';
    mapInfo.innerHTML = `
        <div class="map-overlay-title">Інформація</div>
        <div class="map-overlay-content">
            <p>Інтерактивна карта оперативної обстановки з відображенням інцидентів та розташування підрозділів НГУ.</p>
            <p>Використовуйте колесо миші для масштабування та перетягування для переміщення карти.</p>
        </div>
    `;
    
    // Додаємо інформаційну панель до контейнера карти
    mapElement.parentNode.appendChild(mapInfo);
}