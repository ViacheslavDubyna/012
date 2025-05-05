#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль предикторів для інформаційно-аналітичної системи НГУ

Цей модуль містить класи для прогнозування різних типів даних
за допомогою моделей машинного навчання.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

from . import load_model, save_model


class IncidentPredictor:
    """Клас для прогнозування інцидентів """
    
    def __init__(self):
        """Ініціалізація предиктора інцидентів"""
        self.model = load_model('incident_predictor')
        self.scaler = load_model('incident_scaler')
        
        # Якщо модель не знайдена, створюємо нову
        if self.model is None:
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.scaler = StandardScaler()
    
    def train(self, X, y):
        """Навчання моделі на нових даних"""
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        
        # Зберігаємо навчену модель
        save_model(self.model, 'incident_predictor')
        save_model(self.scaler, 'incident_scaler')
        
        return self
    
    def predict(self, features):
        """Прогнозування рівня загрози інцидентів"""
        if self.model is None:
            return "Модель не навчена"
        
        # Перетворюємо вхідні дані
        features_scaled = self.scaler.transform(features)
        
        # Отримуємо прогноз
        prediction = self.model.predict(features_scaled)
        probabilities = self.model.predict_proba(features_scaled)
        
        # Повертаємо результат
        return {
            'prediction': prediction.tolist(),
            'probabilities': probabilities.tolist()
        }


class NGUIncidentPredictor:
    """Клас для прогнозування кількості інцидентів громадського порядку"""
    
    def __init__(self):
        """Ініціалізація предиктора інцидентів НГУ"""
        self.model = load_model('ngu_incident_predictor')
        self.scaler = load_model('ngu_incident_scaler')
        
        # Якщо модель не знайдена, створюємо нову
        if self.model is None:
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.scaler = StandardScaler()
    
    def train(self, X, y):
        """Навчання моделі на нових даних"""
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        
        # Зберігаємо навчену модель
        save_model(self.model, 'ngu_incident_predictor')
        save_model(self.scaler, 'ngu_incident_scaler')
        
        return self
    
    def predict(self, features):
        """Прогнозування кількості інцидентів громадського порядку"""
        if self.model is None:
            return "Модель не навчена"
        
        # Перетворюємо вхідні дані
        features_scaled = self.scaler.transform(features)
        
        # Отримуємо прогноз
        prediction = self.model.predict(features_scaled)
        
        # Повертаємо результат
        return {
            'prediction': prediction.tolist()
        }


class ResourcePredictor:
    """Клас для прогнозування необхідних ресурсів"""
    
    def __init__(self):
        """Ініціалізація предиктора ресурсів"""
        self.model = load_model('resource_predictor')
        self.scaler = load_model('resource_scaler')
        
        # Якщо модель не знайдена, створюємо нову
        if self.model is None:
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.scaler = StandardScaler()
    
    def train(self, X, y):
        """Навчання моделі на нових даних"""
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        
        # Зберігаємо навчену модель
        save_model(self.model, 'resource_predictor')
        save_model(self.scaler, 'resource_scaler')
        
        return self
    
    def predict(self, features):
        """Прогнозування необхідних ресурсів"""
        if self.model is None:
            return "Модель не навчена"
        
        # Перетворюємо вхідні дані
        features_scaled = self.scaler.transform(features)
        
        # Отримуємо прогноз
        prediction = self.model.predict(features_scaled)
        
        # Повертаємо результат
        return {
            'prediction': prediction.tolist()
        }


def generate_forecast(days=7):
    """Генерація прогнозу на вказану кількість днів"""
    # Це заглушка для демонстрації, в реальній системі тут буде
    # використовуватись навчена модель для прогнозування
    
    today = datetime.now()
    forecast = []
    
    for i in range(days):
        date = today + timedelta(days=i)
        forecast.append({
            'date': date.strftime('%Y-%m-%d'),
            'incident_risk': np.random.choice(['низький', 'середній', 'високий'], p=[0.7, 0.2, 0.1]),
            'ngu_incidents': int(np.random.normal(100, 30)),
            'required_personnel': int(np.random.normal(50, 10))
        })
    
    return forecast