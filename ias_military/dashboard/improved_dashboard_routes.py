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
def init_dash(flask_app):
    """Ініціалізація Dash-додатку в Flask-додатку за допомогою init_app"""
    # Використовуємо init_app для правильної інтеграції
    # Налаштування, такі як suppress_callback_exceptions, title, etc., 
    # вже встановлені в конструкторі Dash у improved_dashboard_integration.py
    dash_app.init_app(flask_app)
    
    # Налаштування, які потрібно встановити після init_app (якщо є)
    # dash_app.config.suppress_callback_exceptions = True # Вже встановлено
    # dash_app.title = 'Інформаційно-аналітична система НГУ' # Вже встановлено

    # Немає необхідності повертати dispatcher, init_app налаштовує маршрутизацію
    # return flask_app # Повертаємо сам flask_app, оскільки Dash інтегровано