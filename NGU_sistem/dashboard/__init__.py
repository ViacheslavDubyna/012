#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль дашборду для інформаційно-аналітичної системи ДПСУ

Цей модуль містить веб-інтерфейс для візуалізації даних та управління системою.
"""

from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__)

# Імпортуємо маршрути дашборду після створення blueprint
from ias_DPSU.dashboard.routes import *