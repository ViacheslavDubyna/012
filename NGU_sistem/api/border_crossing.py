#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API-ендпоінти для даних про перетин кордону

Цей модуль містить API-ендпоінти для отримання статистичних даних 
про перетин кордону для аналітичних інструментів.
"""

from flask import jsonify, request, current_app
from ias_DPSU.api import api_bp
import datetime
import random


@api_bp.route('/border_crossing_trends', methods=['GET'])
def get_border_crossing_trends():
    """Отримання даних про тенденції перетину кордону за останні 30 днів"""
    # В реальній системі ці дані будуть отримуватися з бази даних
    # Зараз генеруємо тестові дані для демонстрації
    
    # Отримуємо поточну дату
    today = datetime.datetime.now()
    
    # Генеруємо дати за останні 30 днів
    dates = [(today - datetime.timedelta(days=i)).strftime('%d.%m.%Y') for i in range(30, 0, -1)]
    
    # Генеруємо випадкові дані для різних категорій
    ukrainian_citizens = [random.randint(3000, 7000) for _ in range(30)]
    foreign_citizens = [random.randint(1000, 3000) for _ in range(30)]
    vehicles = [random.randint(1500, 4000) for _ in range(30)]
    
    # Додаємо тренд зростання для більш реалістичних даних
    for i in range(1, 30):
        # Додаємо невеликий тренд зростання для громадян України
        ukrainian_citizens[i] = max(3000, min(7000, ukrainian_citizens[i-1] + random.randint(-200, 300)))
        
        # Додаємо невеликий тренд зниження для іноземних громадян
        foreign_citizens[i] = max(1000, min(3000, foreign_citizens[i-1] + random.randint(-150, 100)))
        
        # Додаємо невеликий тренд зростання для транспортних засобів
        vehicles[i] = max(1500, min(4000, vehicles[i-1] + random.randint(-100, 200)))
    
    return jsonify({
        'status': 'success',
        'dates': dates,
        'ukrainian_citizens': ukrainian_citizens,
        'foreign_citizens': foreign_citizens,
        'vehicles': vehicles
    })