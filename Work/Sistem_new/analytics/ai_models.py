#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль з AI-моделями для прогнозування загроз та можливих втрат.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report
import logging
import pickle
import os
from datetime import datetime, timedelta
import random

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('ai_models')

# Шлях до збережених моделей
MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

# Шляхи до файлів моделей
THREAT_MODEL_PATH = os.path.join(MODELS_DIR, 'threat_model.pkl')
CASUALTIES_MODEL_PATH = os.path.join(MODELS_DIR, 'casualties_model.pkl')

# Клас для прогнозування загроз
class ThreatPredictor:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.is_trained = False
    
    def train(self, data):
        """
        Навчання моделі для прогнозування загроз
        """
        try:
            if data is None or len(data) < 10:
                logger.warning("Недостатньо даних для навчання моделі прогнозування загроз")
                return False
            
            # Підготовка даних
            X = data[['location', 'incident_type', 'threat_level', 'casualties', 'wounded']]
            y = (data['threat_level'] >= 4).astype(int)  # Бінарна класифікація: 1 - висока загроза, 0 - низька загроза
            
            # Розділення на тренувальну та тестову вибірки
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Препроцесор для категоріальних та числових ознак
            categorical_features = ['location', 'incident_type']
            numeric_features = ['casualties', 'wounded']
            
            categorical_transformer = Pipeline(steps=[
                ('onehot', OneHotEncoder(handle_unknown='ignore'))
            ])
            
            numeric_transformer = Pipeline(steps=[
                ('scaler', StandardScaler())
            ])
            
            self.preprocessor = ColumnTransformer(
                transformers=[
                    ('cat', categorical_transformer, categorical_features),
                    ('num', numeric_transformer, numeric_features)
                ])
            
            # Створення та навчання моделі
            self.model = Pipeline(steps=[
                ('preprocessor', self.preprocessor),
                ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
            ])
            
            self.model.fit(X_train, y_train)
            
            # Оцінка моделі
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            logger.info(f"Точність моделі прогнозування загроз: {accuracy:.2f}")
            
            # Збереження моделі
            with open(THREAT_MODEL_PATH, 'wb') as f:
                pickle.dump(self.model, f)
            
            self.is_trained = True
            return True
        except Exception as e:
            logger.error(f"Помилка при навчанні моделі прогнозування загроз: {e}")
            return False
    
    def load_model(self):
        """
        Завантаження збереженої моделі
        """
        try:
            if os.path.exists(THREAT_MODEL_PATH):
                with open(THREAT_MODEL_PATH, 'rb') as f:
                    self.model = pickle.load(f)
                self.is_trained = True
                logger.info("Модель прогнозування загроз успішно завантажена")
                return True
            else:
                logger.warning("Збережена модель прогнозування загроз не знайдена")
                return False
        except Exception as e:
            logger.error(f"Помилка при завантаженні моделі прогнозування загроз: {e}")
            return False
    
    def predict(self, data):
        """
        Прогнозування загроз на основі нових даних
        """
        try:
            if not self.is_trained:
                if not self.load_model():
                    logger.warning("Модель не навчена і не може бути завантажена. Використання імітаційних даних.")
                    return self._generate_mock_predictions(data)
            
            # Підготовка даних для прогнозування
            X = data[['location', 'incident_type', 'threat_level', 'casualties', 'wounded']]
            
            # Прогнозування ймовірностей
            probabilities = self.model.predict_proba(X)[:, 1]  # Ймовірність високої загрози
            
            # Формування результатів
            results = []
            for i, row in X.iterrows():
                probability = probabilities[i] * 100  # Переведення в відсотки
                expected_casualties = int(probability / 20) if probability > 50 else 0
                
                results.append({
                    'location': row['location'],
                    'threat_type': row['incident_type'],
                    'probability': probability,
                    'expected_casualties': expected_casualties
                })
            
            return results
        except Exception as e:
            logger.error(f"Помилка при прогнозуванні загроз: {e}")
            return self._generate_mock_predictions(data)
    
    def _generate_mock_predictions(self, data):
        """
        Генерація імітаційних прогнозів, якщо модель недоступна
        """
        locations = data['location'].unique() if 'location' in data else ['Харків', 'Донецьк', 'Луганськ', 'Запоріжжя']
        incident_types = data['incident_type'].unique() if 'incident_type' in data else ['Артилерійський обстріл', 'Ракетний удар', 'Атака БПЛА']
        
        results = []
        for location in locations[:4]:  # Обмеження кількості локацій
            for incident_type in incident_types[:2]:  # Обмеження кількості типів інцидентів
                probability = random.uniform(10, 95)
                expected_casualties = int(probability / 20) if probability > 50 else 0
                
                results.append({
                    'location': location,
                    'threat_type': incident_type,
                    'probability': probability,
                    'expected_casualties': expected_casualties
                })
        
        return results

# Клас для прогнозування втрат
class CasualtiesPredictor:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.is_trained = False
    
    def train(self, data):
        """
        Навчання моделі для прогнозування втрат
        """
        try:
            if data is None or len(data) < 10:
                logger.warning("Недостатньо даних для навчання моделі прогнозування втрат")
                return False
            
            # Підготовка даних
            X = data[['location', 'incident_type', 'threat_level']]
            y = data[['casualties', 'wounded']]
            
            # Розділення на тренувальну та тестову вибірки
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Препроцесор для категоріальних та числових ознак
            categorical_features = ['location', 'incident_type']
            numeric_features = ['threat_level']
            
            categorical_transformer = Pipeline(steps=[
                ('onehot', OneHotEncoder(handle_unknown='ignore'))
            ])
            
            numeric_transformer = Pipeline(steps=[
                ('scaler', StandardScaler())
            ])
            
            self.preprocessor = ColumnTransformer(
                transformers=[
                    ('cat', categorical_transformer, categorical_features),
                    ('num', numeric_transformer, numeric_features)
                ])
            
            # Створення та навчання моделі
            self.model = Pipeline(steps=[
                ('preprocessor', self.preprocessor),
                ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
            ])
            
            self.model.fit(X_train, y_train)
            
            # Оцінка моделі
            y_pred = self.model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            logger.info(f"Середньоквадратична помилка моделі прогнозування втрат: {mse:.2f}")
            
            # Збереження моделі
            with open(CASUALTIES_MODEL_PATH, 'wb') as f:
                pickle.dump(self.model, f)
            
            self.is_trained = True
            return True
        except Exception as e:
            logger.error(f"Помилка при навчанні моделі прогнозування втрат: {e}")
            return False
    
    def load_model(self):
        """
        Завантаження збереженої моделі
        """
        try:
            if os.path.exists(CASUALTIES_MODEL_PATH):
                with open(CASUALTIES_MODEL_PATH, 'rb') as f:
                    self.model = pickle.load(f)
                self.is_trained = True
                logger.info("Модель прогнозування втрат успішно завантажена")
                return True
            else:
                logger.warning("Збережена модель прогнозування втрат не знайдена")
                return False
        except Exception as e:
            logger.error(f"Помилка при завантаженні моделі прогнозування втрат: {e}")
            return False
    
    def predict(self, location, incident_type, threat_level):
        """
        Прогнозування втрат на основі нових даних
        """
        try:
            if not self.is_trained:
                if not self.load_model():
                    logger.warning("Модель не навчена і не може бути завантажена. Використання імітаційних даних.")
                    return self._generate_mock_casualties(threat_level)
            
            # Підготовка даних для прогнозування
            X = pd.DataFrame({
                'location': [location],
                'incident_type': [incident_type],
                'threat_level': [threat_level]
            })
            
            # Прогнозування втрат
            predictions = self.model.predict(X)[0]
            
            return {
                'casualties': int(max(0, predictions[0])),
                'wounded': int(max(0, predictions[1]))
            }
        except Exception as e:
            logger.error(f"Помилка при прогнозуванні втрат: {e}")
            return self._generate_mock_casualties(threat_level)
    
    def _generate_mock_casualties(self, threat_level):
        """
        Генерація імітаційних прогнозів втрат, якщо модель недоступна
        """
        casualties = int((threat_level / 5) * random.uniform(0, 3))
        wounded = int((threat_level / 5) * random.uniform(1, 6))
        
        return {
            'casualties': casualties,
            'wounded': wounded
        }

# Функції для використання в інших модулях
def predict_threats(data):
    """
    Прогнозування загроз на основі даних
    """
    predictor = ThreatPredictor()
    
    # Спроба навчити модель, якщо є достатньо даних
    if data is not None and len(data) >= 20:
        predictor.train(data)
    
    # Прогнозування загроз
    return predictor.predict(data)

def simulate_scenario(location, threat_type, intensity):
    """
    Моделювання сценарію з заданими параметрами
    """
    # Конвертація типу загрози в читабельний формат
    threat_type_readable = {
        'artillery': 'Артилерійський обстріл',
        'rocket': 'Ракетний удар',
        'drone': 'Атака БПЛА',
        'mortar': 'Мінометний обстріл',
        'sniper': 'Снайперський вогонь'
    }.get(threat_type, threat_type)
    
    # Розрахунок рівня загрози на основі інтенсивності
    threat_level = min(5, int(intensity / 2))
    
    # Прогнозування втрат
    casualties_predictor = CasualtiesPredictor()
    casualties = casualties_predictor.predict(location, threat_type_readable, threat_level)
    
    # Розрахунок рівня ризику
    risk_level = min(10, intensity + random.randint(-1, 2))
    
    # Генерація рекомендацій
    recommendations = []
    if risk_level >= 7:
        recommendations.append("Негайна евакуація особового складу з небезпечної зони")
        recommendations.append("Розгортання додаткових медичних пунктів")
    elif risk_level >= 4:
        recommendations.append("Посилення оборонних позицій")
        recommendations.append("Підготовка до можливої евакуації")
    else:
        recommendations.append("Підвищення рівня готовності")
        recommendations.append("Посилення розвідки")
    
    return {
        'location': location,
        'threat_type': threat_type_readable,
        'intensity': intensity,
        'risk_level': risk_level,
        'expected_casualties': casualties['casualties'],
        'expected_wounded': casualties['wounded'],
        'recommendations': ", ".join(recommendations)
    }

# Головна функція для тестування модуля
def main():
    logger.info("Тестування модуля AI-моделей...")
    
    # Створення тестових даних
    data = pd.DataFrame({
        'location': ['Харків', 'Донецьк', 'Луганськ', 'Запоріжжя'] * 5,
        'incident_type': ['Артилерійський обстріл', 'Ракетний удар', 'Атака БПЛА', 'Мінометний обстріл', 'Снайперський вогонь'] * 4,
        'threat_level': [random.randint(1, 5) for _ in range(20)],
        'casualties': [random.randint(0, 5) for _ in range(20)],
        'wounded': [random.randint(0, 10) for _ in range(20)]
    })
    
    # Тестування прогнозування загроз
    logger.info("Тестування прогнозування загроз...")
    threat_predictions = predict_threats(data)
    logger.info(f"Отримано {len(threat_predictions)} прогнозів загроз")
    
    # Тестування моделювання сценарію
    logger.info("Тестування моделювання сценарію...")
    scenario_result = simulate_scenario('Харків', 'artillery', 7)
    logger.info(f"Результат моделювання сценарію: {scenario_result}")
    
    logger.info("Тестування модуля AI-моделей завершено")

if __name__ == "__main__":
    main()