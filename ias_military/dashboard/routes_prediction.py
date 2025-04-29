# Маршрути для інструментів прогнозування для інформаційно-аналітичної системи Національної гвардії України

from flask import render_template, request, jsonify
from . import dashboard
import json
import sys
import os

# Додаємо шлях до батьківської директорії в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Імпортуємо аналітичний модуль
from api.analytics import NGUAnalytics

# Ініціалізуємо аналітичний модуль
analytics = NGUAnalytics()

@dashboard.route('/prediction-tools')
def prediction_tools():
    """Сторінка інструментів прогнозування"""
    try:
        return render_template('prediction_tools.html')
    except Exception as e:
        return f'Помилка при завантаженні сторінки інструментів прогнозування: {str(e)}', 500

@dashboard.route('/resource-management')
def resource_management():
    """Сторінка управління ресурсами"""
    try:
        return render_template('resource_management.html')
    except Exception as e:
        return f'Помилка при завантаженні сторінки управління ресурсами: {str(e)}', 500