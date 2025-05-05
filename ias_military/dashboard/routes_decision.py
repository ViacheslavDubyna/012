# Маршрути для підтримки прийняття рішень для інформаційно-аналітичної системи Національної гвардії України

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

@dashboard.route('/decision-effectiveness', methods=['GET'])
def decision_effectiveness():
    """Сторінка підтримки прийняття рішень"""
    try:
        return render_template('decision_effectiveness.html')
    except Exception as e:
        return f'Помилка при завантаженні сторінки підтримки прийняття рішень: {str(e)}', 500

@dashboard.route('/settings', methods=['GET'])
def settings():
    """Сторінка налаштувань системи"""
    try:
        return render_template('settings.html')
    except Exception as e:
        return f'Помилка при завантаженні сторінки налаштувань: {str(e)}', 500