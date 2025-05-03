#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль API для інформаційно-аналітичної системи ДПСУ

Цей модуль містить API-ендпоінти для доступу до даних та функціональності системи.
"""

from flask import Blueprint

api_bp = Blueprint('api', __name__)

# Імпортуємо маршрути API після створення blueprint
from ias_DPSU.api.routes import *
# Явно імпортуємо модуль з ендпоінтами для даних про перетин кордону
from ias_DPSU.api.border_crossing import *
# Імпортуємо модуль з ендпоінтами для прогнозів перетину кордону
from ias_DPSU.api.predictions import *