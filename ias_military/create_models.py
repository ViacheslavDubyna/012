# Скрипт для створення порожніх ML-моделей для інформаційно-аналітичної системи

import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

# Шлях до директорії з моделями
MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')

# Перевірка наявності директорії
if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)
    print(f"Створено директорію для моделей: {MODELS_DIR}")

# Створення порожніх моделей
def create_empty_models():
    # Створюємо прості моделі для основних предикторів
    models = {
        'threat_predictor': RandomForestClassifier(n_estimators=10),
        'resource_predictor': RandomForestRegressor(n_estimators=10),
        'incident_predictor': RandomForestClassifier(n_estimators=10)
    }
    
    # Тренуємо моделі на мінімальних даних для можливості серіалізації
    X = np.array([[0, 0], [1, 1], [2, 2]])
    y_class = np.array([0, 1, 0])
    y_reg = np.array([0.1, 0.5, 0.9])
    
    # Навчаємо класифікатори
    models['threat_predictor'].fit(X, y_class)
    models['incident_predictor'].fit(X, y_class)
    
    # Навчаємо регресор
    models['resource_predictor'].fit(X, y_reg)
    
    # Зберігаємо моделі
    for model_name, model in models.items():
        model_path = os.path.join(MODELS_DIR, f"{model_name}.joblib")
        try:
            joblib.dump(model, model_path)
            print(f"Модель {model_name} успішно створена та збережена в {model_path}")
        except Exception as e:
            print(f"Помилка збереження моделі {model_name}: {e}")

if __name__ == '__main__':
    print("Створення порожніх ML-моделей для інформаційно-аналітичної системи...")
    create_empty_models()
    print("Готово! Моделі створено та збережено.")