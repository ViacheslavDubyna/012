#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль ML-моделей для інформаційно-аналітичної системи ДПСУ

Цей модуль містить класи та функції для роботи з моделями машинного навчання,
які використовуються для прогнозування та аналізу даних.
"""

import os
import joblib
from ias_DPSU.config.config import Config

# Шлях до директорії з моделями
MODELS_DIR = Config.MODELS_DIR

# Перевіряємо, чи існує директорія для моделей, якщо ні - створюємо
if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

# Функція для завантаження моделі
def load_model(model_name):
    """Завантаження ML-моделі з файлу"""
    model_path = os.path.join(MODELS_DIR, f"{model_name}.joblib")
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        return None

# Функція для збереження моделі
def save_model(model, model_name):
    """Збереження ML-моделі у файл"""
    model_path = os.path.join(MODELS_DIR, f"{model_name}.joblib")
    joblib.dump(model, model_path)
    return model_path