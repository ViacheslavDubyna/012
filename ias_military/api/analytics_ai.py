# Модуль AI-аналітики для прогнозування оперативної обстановки та потреб у ресурсах

import os
import sys
import numpy as np
import pandas as pd
import joblib
import datetime
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report

# Додаємо шлях до батьківської директорії в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Імпортуємо конфігурацію та аналітичний модуль
from config.config import MODELS_DIR
from api.analytics import NGUAnalytics

class AIPredictor:
    def __init__(self):
        self.analytics = NGUAnalytics()
        self.models = {}
        self.load_models()
    
    def load_models(self):
        """Завантаження збережених моделей"""
        model_files = {
            'threat_predictor': os.path.join(MODELS_DIR, 'threat_predictor.joblib'),
            'resource_predictor': os.path.join(MODELS_DIR, 'resource_predictor.joblib'),
            'incident_predictor': os.path.join(MODELS_DIR, 'incident_predictor.joblib')
        }
        
        models_loaded = False
        for model_name, model_path in model_files.items():
            if os.path.exists(model_path):
                try:
                    # Перевірка розміру файлу - якщо менше 1KB, ймовірно це заглушка
                    file_size = os.path.getsize(model_path)
                    if file_size < 1024:  # менше 1KB
                        try:
                            # Спробуємо відкрити як текстовий файл
                            with open(model_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read(100)  # Читаємо перші 100 символів
                                if '#' in content or 'заглушка' in content:
                                    print(f"Файл {model_name} є заглушкою, буде створена нова модель при навчанні")
                                    continue
                        except UnicodeDecodeError:
                            # Якщо не вдалося відкрити як текст, спробуємо як бінарний
                            pass
                    
                    # Спробуємо завантажити модель
                    self.models[model_name] = joblib.load(model_path)
                    print(f"Модель {model_name} успішно завантажена")
                    models_loaded = True
                except Exception as e:
                    print(f"Помилка завантаження моделі {model_name}: {e}")
                    # Продовжуємо роботу без цієї моделі
            else:
                print(f"Модель {model_name} не знайдена, буде створена при навчанні")
        
        if not models_loaded:
            print("Не знайдено жодної робочої моделі для завантаження. Моделі будуть створені при першому використанні.")
            # Ініціалізуємо порожні моделі для уникнення помилок
            self.initialize_empty_models()
    
    def initialize_empty_models(self):
        """Ініціалізація порожніх моделей для уникнення помилок"""
        # Створюємо прості моделі-заглушки для основних предикторів
        self.models['threat_predictor'] = RandomForestClassifier(n_estimators=10)
        self.models['resource_predictor'] = RandomForestRegressor(n_estimators=10)
        self.models['incident_predictor'] = RandomForestClassifier(n_estimators=10)
        print("Ініціалізовано порожні моделі-заглушки для роботи системи")
    
    def save_model(self, model_name, model):
        """Збереження моделі"""
        model_path = os.path.join(MODELS_DIR, f"{model_name}.joblib")
        try:
            joblib.dump(model, model_path)
            self.models[model_name] = model
            print(f"Модель {model_name} успішно збережена")
            return True
        except Exception as e:
            print(f"Помилка збереження моделі {model_name}: {e}")
            return False
    
    def train_threat_predictor(self):
        """Навчання моделі для прогнозування рівня загрози"""
        # Отримання та підготовка даних
        data = self.analytics.prepare_threat_prediction_data()
        
        if data.empty:
            print("Недостатньо даних для навчання моделі прогнозування загроз")
            return False
        
        # Визначення ознак та цільової змінної
        features = [
            'hour', 'day', 'month', 'day_of_week',
            'Порушення громадського порядку', 'Терористична загроза', 'Диверсія', 
            'Масові заворушення', 'Блокування об\'єктів', 'avg_severity',
            'total_casualties', 'property_damage_count'
        ]
        
        # Додаємо категоріальні ознаки, якщо вони є в даних
        categorical_features = ['region', 'status']
        for feature in categorical_features:
            if feature in data.columns:
                features.append(feature)
        
        X = data[features]
        y = data['threat_level']
        
        # Розділення даних на тренувальну та тестову вибірки
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Визначення категоріальних та числових ознак
        categorical_features = ['region', 'status']
        categorical_features = [f for f in categorical_features if f in X.columns]
        numerical_features = [f for f in X.columns if f not in categorical_features]
        
        # Створення препроцесора
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numerical_features),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
            ]
        )
        
        # Створення та навчання моделі
        model = Pipeline([
            ('preprocessor', preprocessor),
            ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
        ])
        
        model.fit(X_train, y_train)
        
        # Оцінка моделі
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        print(f"Модель прогнозування загроз - RMSE: {rmse:.4f}")
        
        # Збереження моделі
        return self.save_model('threat_predictor', model)
    
    def train_resource_predictor(self):
        """Навчання моделі для прогнозування потреб у ресурсах"""
        # Отримання та підготовка даних
        situations_df = self.analytics.get_situation_data()
        resources_df = self.analytics.get_resource_data()
        allocations_df = self.analytics.session.query(
            self.analytics.ResourceAllocation
        ).statement
        allocations_df = pd.read_sql(allocations_df, self.analytics.engine)
        
        if situations_df.empty or resources_df.empty or allocations_df.empty:
            print("Недостатньо даних для навчання моделі прогнозування ресурсів")
            return False
        
        # Об'єднання даних
        data = allocations_df.merge(
            situations_df, left_on='situation_id', right_on='id', suffixes=('', '_situation')
        )
        data = data.merge(
            resources_df, left_on='resource_id', right_on='id', suffixes=('', '_resource')
        )
        
        # Визначення ознак та цільової змінної
        features = [
            'threat_level', 'status', 'region', 'type', 'priority'
        ]
        
        # Перетворення категоріальних ознак
        for feature in ['status', 'region', 'type']:
            data[feature] = data[feature].astype('category').cat.codes
        
        X = data[features]
        y = data['quantity_allocated']
        
        # Розділення даних на тренувальну та тестову вибірки
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Створення та навчання моделі
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Оцінка моделі
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        print(f"Модель прогнозування ресурсів - RMSE: {rmse:.4f}")
        
        # Збереження моделі під обома назвами для сумісності
        success = self.save_model('resource_predictor', model)
        
        # Також зберігаємо модель в analytics під назвою resource_need для сумісності
        if hasattr(self.analytics, 'models'):
            self.analytics.models['resource_need'] = model
            print("Модель resource_predictor також збережена як resource_need в analytics для сумісності")
            
        return success
    
    def train_incident_predictor(self):
        """Навчання моделі для прогнозування ймовірності інцидентів"""
        # Отримання та підготовка даних
        situations_df = self.analytics.get_situation_data()
        incidents_df = self.analytics.get_incident_data()
        
        if situations_df.empty or incidents_df.empty:
            print("Недостатньо даних для навчання моделі прогнозування інцидентів")
            return False
        
        # Додаємо часові ознаки
        situations_df['hour'] = situations_df['timestamp'].dt.hour
        situations_df['day'] = situations_df['timestamp'].dt.day
        situations_df['month'] = situations_df['timestamp'].dt.month
        situations_df['day_of_week'] = situations_df['timestamp'].dt.dayofweek
        
        # Створюємо бінарну ознаку наявності інциденту
        situations_df['has_incident'] = situations_df['id'].isin(incidents_df['situation_id']).astype(int)
        
        # Визначення ознак та цільової змінної
        features = [
            'hour', 'day', 'month', 'day_of_week', 'threat_level', 'region', 'status'
        ]
        
        # Перетворення категоріальних ознак
        for feature in ['region', 'status']:
            situations_df[feature] = situations_df[feature].astype('category').cat.codes
        
        X = situations_df[features]
        y = situations_df['has_incident']
        
        # Розділення даних на тренувальну та тестову вибірки
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Створення та навчання моделі
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Оцінка моделі
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Модель прогнозування інцидентів - Точність: {accuracy:.4f}")
        print(classification_report(y_test, y_pred))
        
        # Збереження моделі
        return self.save_model('incident_predictor', model)
    
    def train_all_models(self):
        """Навчання всіх моделей"""
        self.train_threat_predictor()
        self.train_resource_predictor()
        self.train_incident_predictor()
        return True
    
    def predict_threat_level(self, region, location, status, **kwargs):
        """Прогнозування рівня загрози"""
        if 'threat_predictor' not in self.models:
            self.train_threat_predictor()
            if 'threat_predictor' not in self.models:
                return {'error': 'Не вдалося створити модель прогнозування загроз'}
        
        # Підготовка даних для прогнозування
        data = {
            'region': region,
            'status': status,
            'hour': kwargs.get('hour', datetime.datetime.now().hour),
            'day': kwargs.get('day', datetime.datetime.now().day),
            'month': kwargs.get('month', datetime.datetime.now().month),
            'day_of_week': kwargs.get('day_of_week', datetime.datetime.now().weekday()),
            'Порушення громадського порядку': kwargs.get('public_disorder', 0),
            'Терористична загроза': kwargs.get('terrorist_threat', 0),
            'Диверсія': kwargs.get('sabotage', 0),
            'Масові заворушення': kwargs.get('mass_riots', 0),
            'Блокування об\'єктів': kwargs.get('object_blocking', 0),
            'avg_severity': kwargs.get('avg_severity', 0),
            'total_casualties': kwargs.get('casualties', 0),
            'property_damage_count': kwargs.get('property_damage', 0)
        }
        
        # Створення DataFrame для прогнозування
        df = pd.DataFrame([data])
        
        # Прогнозування
        try:
            prediction = self.models['threat_predictor'].predict(df)[0]
            confidence = 0.8  # Спрощена оцінка впевненості
            
            return {
                'threat_level': round(prediction, 2),
                'confidence': confidence,
                'region': region,
                'location': location,
                'status': status,
                'timestamp': datetime.datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Помилка прогнозування рівня загрози: {e}")
            return {'error': str(e)}
    
    def predict_resource_needs(self, situation_id, resource_type, priority=3):
        """Прогнозування потреб у ресурсах"""
        # Перевіряємо наявність моделі під обома можливими назвами
        if 'resource_predictor' not in self.models:
            # Перевіряємо, чи є модель під назвою resource_need в analytics
            if hasattr(self.analytics, 'models') and 'resource_need' in self.analytics.models:
                print("Використовуємо модель resource_need з analytics для сумісності")
                self.models['resource_predictor'] = self.analytics.models['resource_need']
            else:
                # Якщо немає, навчаємо нову модель
                self.train_resource_predictor()
                if 'resource_predictor' not in self.models:
                    return {'error': 'Не вдалося створити модель прогнозування ресурсів'}
        
        # Отримання даних про ситуацію
        situation = self.analytics.session.query(
            self.analytics.OperationalSituation
        ).filter_by(id=situation_id).first()
        
        if not situation:
            return {'error': 'Ситуацію не знайдено'}
        
        # Підготовка даних для прогнозування
        data = {
            'threat_level': situation.threat_level,
            'status': situation.status,
            'region': situation.region,
            'type': resource_type,
            'priority': priority
        }
        
        # Перетворення категоріальних ознак
        status_mapping = {'Штатна': 0, 'Напружена': 1, 'Критична': 2, 'Надзвичайна': 3}
        region_mapping = {'Північ': 0, 'Південь': 1, 'Схід': 2, 'Захід': 3, 'Центр': 4, 'Київ': 5}
        type_mapping = {'Особовий склад': 0, 'Техніка': 1, 'Озброєння': 2, 'Боєприпаси': 3, 'Спорядження': 4}
        
        data['status'] = status_mapping.get(data['status'], 0)
        data['region'] = region_mapping.get(data['region'], 0)
        data['type'] = type_mapping.get(data['type'], 0)
        
        # Створення DataFrame для прогнозування
        df = pd.DataFrame([data])
        
        # Прогнозування
        try:
            prediction = self.models['resource_predictor'].predict(df)[0]
            confidence = 0.75  # Спрощена оцінка впевненості
            
            return {
                'resource_type': resource_type,
                'quantity_needed': max(1, int(round(prediction))),
                'confidence': confidence,
                'situation_id': situation_id,
                'priority': priority,
                'timestamp': datetime.datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Помилка прогнозування потреб у ресурсах: {e}")
            return {'error': str(e)}
    
    def predict_incident_probability(self, region, status, threat_level):
        """Прогнозування ймовірності інцидентів"""
        if 'incident_predictor' not in self.models:
            self.train_incident_predictor()
            if 'incident_predictor' not in self.models:
                return {'error': 'Не вдалося створити модель прогнозування інцидентів'}
        
        # Підготовка даних для прогнозування
        now = datetime.datetime.now()
        data = {
            'hour': now.hour,
            'day': now.day,
            'month': now.month,
            'day_of_week': now.weekday(),
            'threat_level': threat_level,
            'region': region,
            'status': status
        }
        
        # Перетворення категоріальних ознак
        region_mapping = {'Північ': 0, 'Південь': 1, 'Схід': 2, 'Захід': 3, 'Центр': 4, 'Київ': 5}
        status_mapping = {'Штатна': 0, 'Напружена': 1, 'Критична': 2, 'Надзвичайна': 3}
        
        data['region'] = region_mapping.get(data['region'], 0)
        data['status'] = status_mapping.get(data['status'], 0)
        
        # Створення DataFrame для прогнозування
        df = pd.DataFrame([data])
        
        # Прогнозування
        try:
            probability = self.models['incident_predictor'].predict_proba(df)[0][1]
            
            return {
                'incident_probability': round(probability, 4),
                'region': region,
                'status': status,
                'threat_level': threat_level,
                'timestamp': now.isoformat()
            }
        except Exception as e:
            print(f"Помилка прогнозування ймовірності інцидентів: {e}")
            return {'error': str(e)}

# Створення екземпляру класу для використання в API
ai_predictor = AIPredictor()