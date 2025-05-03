#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль бази даних для інформаційно-аналітичної системи ДПСУ

Цей модуль відповідає за взаємодію з базою даних, включаючи підключення,
запити та управління даними.
"""

from flask_sqlalchemy import SQLAlchemy

# Створюємо екземпляр SQLAlchemy для роботи з базою даних
db = SQLAlchemy()

# Імпортуємо моделі даних після створення екземпляру db
from ias_DPSU.database.models import *

def init_app(app):
    """Ініціалізація бази даних для Flask додатку"""
    db.init_app(app)
    
    # Створюємо всі таблиці при запуску додатку, якщо вони не існують
    with app.app_context():
        db.create_all()