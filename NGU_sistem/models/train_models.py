#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль для навчання моделей машинного навчання для інформаційно-аналітичної системи НГУ

Цей модуль використовує згенеровані тестові дані для навчання моделей
прогнозування інцидентів, перетинів кордону та необхідних ресурсів.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_absolute_error, classification_report

from .predictors import IncidentPredictor, BorderCrossingPredictor, ResourcePredictor
from database.generate_test_data import (
    generate_training_data_for_incident_predictor,
    generate_training_data_for_border_crossing_predictor,
    generate_training_data_for_resource_predictor
)


def train_incident_predictor(test_size=0.2, random_state=42):
    """
    Навчання моделі прогнозування інцидентів 
    
    :param test_size: частка тестової вибірки
    :param random_state: початкове значення для генератора випадкових чисел
    :return: навчена модель та метрики якості
    """
    print("Навчання моделі прогнозування інцидентів...")
    
    # Генерація тренувальних даних
    X, y = generate_training_data_for_incident_predictor(count=1000)
    
    # Розділення на тренувальну та тестову вибірки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    # Ініціалізація та навчання моделі
    predictor = IncidentPredictor()
    predictor.train(X_train, y_train)
    
    # Оцінка якості моделі
    features_scaled = predictor.scaler.transform(X_test)
    y_pred = predictor.model.predict(features_scaled)
    
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    # Отримуємо унікальні класи для правильного доступу до звіту
    classes = sorted(list(set(y_test) | set(y_pred)))
    
    print(f"Точність моделі прогнозування інцидентів: {accuracy:.4f}")
    print("Звіт про класифікацію:")
    
    # Відображення метрик для кожного класу
    for cls in classes:
        print(f"- {cls.capitalize()} рівень загрози: F1-score = {report.get(cls, {}).get('f1-score', 0):.4f}")

    
    return predictor, {
        'accuracy': accuracy,
        'classification_report': report
    }


def train_border_crossing_predictor(test_size=0.2, random_state=42):
    """
    Навчання моделі прогнозування кількості інцидентів
    
    :param test_size: частка тестової вибірки
    :param random_state: початкове значення для генератора випадкових чисел
    :return: навчена модель та метрики якості
    """
    print("\nНавчання моделі прогнозування інцидентів...")
    
    # Генерація тренувальних даних
    X, y = generate_training_data_for_border_crossing_predictor(count=1000)
    
    # Розділення на тренувальну та тестову вибірки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    # Ініціалізація та навчання моделі
    predictor = BorderCrossingPredictor()
    predictor.train(X_train, y_train)
    
    # Оцінка якості моделі
    features_scaled = predictor.scaler.transform(X_test)
    y_pred = predictor.model.predict(features_scaled)
    
    mae = mean_absolute_error(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    
    print(f"Середня абсолютна помилка (MAE): {mae:.2f} перетинів")
    print(f"Середня абсолютна відсоткова помилка (MAPE): {mape:.2f}%")
    
    return predictor, {
        'mae': mae,
        'mape': mape
    }


def train_resource_predictor(test_size=0.2, random_state=42):
    """
    Навчання моделі прогнозування необхідних ресурсів
    
    :param test_size: частка тестової вибірки
    :param random_state: початкове значення для генератора випадкових чисел
    :return: навчена модель та метрики якості
    """
    print("\nНавчання моделі прогнозування необхідних ресурсів...")
    
    # Генерація тренувальних даних
    X, y = generate_training_data_for_resource_predictor(count=1000)
    
    # Розділення на тренувальну та тестову вибірки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    # Ініціалізація та навчання моделі
    predictor = ResourcePredictor()
    predictor.train(X_train, y_train)
    
    # Оцінка якості моделі
    features_scaled = predictor.scaler.transform(X_test)
    y_pred = predictor.model.predict(features_scaled)
    
    mae = mean_absolute_error(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    
    print(f"Середня абсолютна помилка (MAE): {mae:.2f} осіб")
    print(f"Середня абсолютна відсоткова помилка (MAPE): {mape:.2f}%")
    
    return predictor, {
        'mae': mae,
        'mape': mape
    }


def train_all_models():
    """
    Навчання всіх моделей прогнозування
    
    :return: словник з навченими моделями та їх метриками
    """
    results = {}
    
    # Навчання моделі прогнозування інцидентів
    incident_predictor, incident_metrics = train_incident_predictor()
    results['incident_predictor'] = {
        'model': incident_predictor,
        'metrics': incident_metrics
    }
    
    # Навчання моделі прогнозування перетинів кордону
    border_crossing_predictor, border_crossing_metrics = train_border_crossing_predictor()
    results['border_crossing_predictor'] = {
        'model': border_crossing_predictor,
        'metrics': border_crossing_metrics
    }
    
    # Навчання моделі прогнозування необхідних ресурсів
    resource_predictor, resource_metrics = train_resource_predictor()
    results['resource_predictor'] = {
        'model': resource_predictor,
        'metrics': resource_metrics
    }
    
    print("\Всі моделі успішно навчені та збережені.")
    
    return results


if __name__ == "__main__":
    # Цей код виконується тільки при прямому запуску скрипта
    from ias_NGU.run import app
    with app.app_context():
        train_all_models()