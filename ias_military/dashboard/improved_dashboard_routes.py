# Маршрути для вдосконаленого дашборду
# Інтеграція Dash-додатку з Flask

from flask import Blueprint, render_template, request, jsonify, current_app
import dash
from dash import html
import sys
import os
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from jinja2 import TemplateNotFound

# Додаємо шлях до батьківської директорії в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Імпортуємо вдосконалений дашборд
from dashboard.improved_dashboard_integration import app as dash_app

# Створюємо Blueprint для маршрутів дашборду
improved_dashboard = Blueprint('improved_dashboard', __name__, template_folder='templates')

@improved_dashboard.route('/')
def index():
    """Головна сторінка вдосконаленого дашборду"""
    try:
        return render_template('dashboard/improved_dashboard.html')
    except TemplateNotFound:
        current_app.logger.error('Відсутній шаблон: improved_dashboard.html')
        return 'Шаблон не знайдено', 404

# Функція для інтеграції Dash-додатку з Flask
def register_dashapp(flask_app):
    """Реєстрація Dash-додатку в Flask-додатку"""
    # Налаштування Dash-додатку для роботи з Flask
    dash_app.config.update({
        'routes_pathname_prefix': '/dashboard/improved/',
        'requests_pathname_prefix': '/dashboard/improved/',
        'suppress_callback_exceptions': True,
        'update_title': 'Завантаження...',
        'external_scripts': [
            'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js'
        ]
    })
    
    # Створюємо DispatcherMiddleware для маршрутизації запитів
    dispatcher = DispatcherMiddleware(flask_app, {
        '/dashboard/improved': dash_app.server
    })
    
    return dispatcher

# Функція для запуску сервера з інтегрованим Dash-додатком
def run_server(flask_app, host='0.0.0.0', port=5000):
    """Запуск сервера з інтегрованим Dash-додатком"""
    dispatcher = register_dashapp(flask_app)
    run_simple(host, port, dispatcher, use_reloader=True, use_debugger=True)