#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API-ендпоінти для прогнозів перетину кордону

Цей модуль містить API-ендпоінти для отримання прогнозних даних 
про перетин кордону на наступний тиждень та місяць.
"""

from flask import jsonify, request, current_app
from ias_DPSU.api import api_bp
import datetime
import random


@api_bp.route('/border_crossing_weekly_prediction', methods=['GET'])
def get_border_crossing_weekly_prediction():
    """Отримання прогнозних даних про перетин кордону на наступний тиждень"""
    # В реальній системі ці дані будуть отримуватися з моделі прогнозування
    # Зараз генеруємо тестові дані для демонстрації
    
    # Отримуємо поточну дату
    today = datetime.datetime.now()
    
    # Генеруємо дати на наступний тиждень
    dates = [(today + datetime.timedelta(days=i)).strftime('%d.%m.%Y') for i in range(1, 8)]
    
    # Генеруємо випадкові дані для різних категорій з трендом зростання
    base_ukrainian = random.randint(4000, 6000)
    base_foreign = random.randint(1500, 2500)
    base_vehicles = random.randint(2000, 3500)
    
    ukrainian_citizens = []
    foreign_citizens = []
    vehicles = []
    
    # Додаємо тренд зростання для більш реалістичних даних
    for i in range(7):
        # Додаємо тренд зростання для громадян України з піком на вихідних
        weekend_factor = 1.3 if i >= 5 else 1.0  # Вихідні дні (субота, неділя)
        ukrainian_citizens.append(int(base_ukrainian * (1 + 0.05 * i) * weekend_factor))
        
        # Додаємо тренд для іноземних громадян
        foreign_citizens.append(int(base_foreign * (1 + 0.03 * i) * weekend_factor))
        
        # Додаємо тренд для транспортних засобів
        vehicles.append(int(base_vehicles * (1 + 0.04 * i) * weekend_factor))
    
    return jsonify({
        'status': 'success',
        'dates': dates,
        'ukrainian_citizens': ukrainian_citizens,
        'foreign_citizens': foreign_citizens,
        'vehicles': vehicles
    })


@api_bp.route('/border_crossing_monthly_prediction', methods=['GET'])
def get_border_crossing_monthly_prediction():
    """Отримання прогнозних даних про перетин кордону на наступний місяць"""
    # В реальній системі ці дані будуть отримуватися з моделі прогнозування
    # Зараз генеруємо тестові дані для демонстрації
    
    # Отримуємо поточну дату
    today = datetime.datetime.now()
    
    # Генеруємо дати на наступний місяць (30 днів)
    dates = [(today + datetime.timedelta(days=i)).strftime('%d.%m.%Y') for i in range(1, 31)]
    
    # Генеруємо випадкові дані для різних категорій з трендом зростання
    base_ukrainian = random.randint(4000, 6000)
    base_foreign = random.randint(1500, 2500)
    base_vehicles = random.randint(2000, 3500)
    
    ukrainian_citizens = []
    foreign_citizens = []
    vehicles = []
    
    # Додаємо тренд зростання для більш реалістичних даних
    for i in range(30):
        # Додаємо сезонність - вихідні дні мають більше перетинів
        day_of_week = (today.weekday() + i) % 7
        weekend_factor = 1.3 if day_of_week >= 5 else 1.0  # Вихідні дні (субота, неділя)
        
        # Додаємо тренд зростання для громадян України
        trend_factor = 1 + (0.01 * i) + (0.1 * (i // 7))  # Поступове зростання з тижневими стрибками
        ukrainian_citizens.append(int(base_ukrainian * trend_factor * weekend_factor))
        
        # Додаємо тренд для іноземних громадян
        foreign_trend = 1 + (0.005 * i) + (0.05 * (i // 7))
        foreign_citizens.append(int(base_foreign * foreign_trend * weekend_factor))
        
        # Додаємо тренд для транспортних засобів
        vehicle_trend = 1 + (0.008 * i) + (0.07 * (i // 7))
        vehicles.append(int(base_vehicles * vehicle_trend * weekend_factor))
    
    return jsonify({
        'status': 'success',
        'dates': dates,
        'ukrainian_citizens': ukrainian_citizens,
        'foreign_citizens': foreign_citizens,
        'vehicles': vehicles
    })