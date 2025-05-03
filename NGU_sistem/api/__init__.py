#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль API для інформаційно-аналітичної системи НГУ

Цей модуль містить API-ендпоінти для доступу до даних та функціональності системи.
"""

from flask import Blueprint

api_bp = Blueprint('api', __name__)

# Імпортуємо маршрути API після створення blueprint
from .routes import *
from .border_crossing import *
from .predictions import *