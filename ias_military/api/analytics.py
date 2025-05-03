# Модуль аналітики та прогнозування для інформаційно-аналітичної системи Національної гвардії України

import os
import sys
import pandas as pd
import numpy as np
import datetime
from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report
import joblib

# Додаємо шлях до батьківської директорії в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Імпортуємо моделі бази даних
from database.models import OperationalSituation, Resource, ResourceAllocation, Incident, Decision, Prediction, NGUUnit

# Імпортуємо конфігурацію бази даних
from config.config import DB_URL

class NGUAnalytics:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(NGUAnalytics, cls).__new__(cls)
        return cls._instance
    def __init__(self, db_url=DB_URL, models_dir='models'):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.engine = create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.models = {}
        self.models_dir = models_dir
        from flask import current_app
        try:
            disable_ml = current_app.config.get('DISABLE_ML', False)
            if disable_ml:
                print("ML-функціонал вимкнено. Моделі не будуть завантажені.")
                self._initialized = True
                return
        except RuntimeError:
            pass
        self.load_models(models_dir)
        self._initialized = True
    
    def get_situation_data(self):
        """Отримання даних про оперативну обстановку"""
        query = self.session.query(OperationalSituation).order_by(OperationalSituation.timestamp)
        df = pd.read_sql(query.statement, self.engine)
        return df
    
    def get_resource_data(self):
        """Отримання даних про ресурси"""
        query = self.session.query(Resource)
        df = pd.read_sql(query.statement, self.engine)
        return df
    
    def get_incident_data(self):
        """Отримання даних про інциденти"""
        query = self.session.query(Incident).order_by(Incident.timestamp)
        df = pd.read_sql(query.statement, self.engine)
        return df
    
    def get_decision_data(self):
        """Отримання даних про рішення"""
        query = self.session.query(Decision).order_by(Decision.decision_time)
        df = pd.read_sql(query.statement, self.engine)
        return df
    
    def get_prediction_data(self):
        """Отримання даних про прогнози"""
        query = self.session.query(Prediction).order_by(Prediction.timestamp)
        df = pd.read_sql(query.statement, self.engine)
        return df
    
    def prepare_threat_prediction_data(self):
        """Підготовка даних для прогнозування рівня загрози для підрозділів НГУ"""
        # Отримуємо дані про оперативну обстановку та інциденти
        situations_df = self.get_situation_data()
        incidents_df = self.get_incident_data()
        
        # Додаємо часові ознаки
        situations_df['hour'] = situations_df['timestamp'].dt.hour
        situations_df['day'] = situations_df['timestamp'].dt.day
        situations_df['month'] = situations_df['timestamp'].dt.month
        situations_df['day_of_week'] = situations_df['timestamp'].dt.dayofweek
        
        # Рахуємо кількість інцидентів для кожної ситуації за типами
        incident_counts = incidents_df.groupby(['situation_id', 'type']).size().unstack(fill_value=0).reset_index()
        incident_counts.columns.name = None
        
        # Якщо немає даних про певні типи інцидентів, створюємо порожні стовпці
        incident_types = ['Порушення громадського порядку', 'Терористична загроза', 'Диверсія', 'Масові заворушення', 'Блокування об\'єктів']
        for incident_type in incident_types:
            if incident_type not in incident_counts.columns:
                incident_counts[incident_type] = 0
        
        # Рахуємо середню серйозність інцидентів для кожної ситуації
        incident_severity = incidents_df.groupby('situation_id')['severity'].mean().reset_index(name='avg_severity')
        
        # Рахуємо кількість постраждалих
        casualties = incidents_df.groupby('situation_id')['casualties'].sum().reset_index(name='total_casualties')
        
        # Рахуємо кількість інцидентів з пошкодженням майна
        property_damage = incidents_df.groupby('situation_id')['property_damage'].sum().reset_index(name='property_damage_count')
        
        # Об'єднуємо дані
        df = situations_df.merge(incident_counts, left_on='id', right_on='situation_id', how='left')
        df = df.merge(incident_severity, left_on='id', right_on='situation_id', how='left')
        df = df.merge(casualties, left_on='id', right_on='situation_id', how='left')
        df = df.merge(property_damage, left_on='id', right_on='situation_id', how='left')
        
        # Заповнюємо пропущені значення
        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                df[col] = df[col].fillna(0)
        
        # Додаємо ознаку готовності підрозділу
        units_df = pd.read_sql(self.session.query(NGUUnit).statement, self.engine)
        df = df.merge(units_df[['id', 'readiness_level']], left_on='unit_id', right_on='id', how='left', suffixes=('', '_unit'))
        df['readiness_level'] = df['readiness_level'].fillna(3)  # Середній рівень за замовчуванням
        
        # Створюємо цільову змінну (високий рівень загрози чи ні)
        df['high_threat'] = (df['threat_level'] >= 4).astype(int)
        
        # Вибираємо ознаки та цільову змінну
        features = [
            'hour', 'day', 'month', 'day_of_week', 
            'Порушення громадського порядку', 'Терористична загроза', 'Диверсія', 'Масові заворушення', 'Блокування об\'єктів',
            'avg_severity', 'total_casualties', 'property_damage_count', 'readiness_level', 'region', 'location', 'status'
        ]
        
        # Перевіряємо наявність всіх стовпців
        for feature in features:
            if feature not in df.columns:
                if feature in incident_types:
                    df[feature] = 0
                else:
                    print(f"Відсутня ознака: {feature}")
        
        X = df[features]
        y = df['high_threat']
        
        return X, y
    
    def train_threat_prediction_model(self):
        """Навчання моделі для прогнозування рівня загрози для підрозділів НГУ"""
        X, y = self.prepare_threat_prediction_data()
        
        # Розділяємо дані на тренувальну та тестову вибірки
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Визначаємо числові та категоріальні ознаки
        numeric_features = [
            'hour', 'day', 'month', 'day_of_week', 
            'Порушення громадського порядку', 'Терористична загроза', 'Диверсія', 'Масові заворушення', 'Блокування об\'єктів',
            'avg_severity', 'total_casualties', 'property_damage_count', 'readiness_level'
        ]
        categorical_features = ['region', 'location', 'status']
        
        # Створюємо препроцесори для різних типів ознак
        numeric_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])
        
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        
        # Об'єднуємо препроцесори
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])
        
        # Створюємо пайплайн з препроцесором та моделлю
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        
        # Навчаємо модель
        model.fit(X_train, y_train)
        
        # Оцінюємо модель
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        print(f"Точність моделі прогнозування рівня загрози: {accuracy:.4f}")
        print(report)
        
        # Зберігаємо модель
        self.models['threat_prediction'] = model
        
        return model, accuracy, report
    
    def prepare_resource_need_data(self):
        """Підготовка даних для прогнозування потреб у ресурсах для підрозділів НГУ"""
        # Отримуємо дані про оперативну обстановку, інциденти та ресурси
        situations_df = self.get_situation_data()
        incidents_df = self.get_incident_data()
        resources_df = self.get_resource_data()
        
        # Отримуємо дані про підрозділи НГУ
        units_df = pd.read_sql(self.session.query(NGUUnit).statement, self.engine)
        
        # Додаємо дані про розподіл ресурсів
        allocations_df = pd.read_sql(self.session.query(ResourceAllocation).statement, self.engine)
        
        # Рахуємо кількість інцидентів для кожної ситуації за типами
        incident_counts = incidents_df.groupby(['situation_id', 'type']).size().unstack(fill_value=0).reset_index()
        incident_counts.columns.name = None
        
        # Якщо немає даних про певні типи інцидентів, створюємо порожні стовпці
        incident_types = ['Порушення громадського порядку', 'Терористична загроза', 'Диверсія', 'Масові заворушення', 'Блокування об\'єктів']
        for incident_type in incident_types:
            if incident_type not in incident_counts.columns:
                incident_counts[incident_type] = 0
        
        # Рахуємо середню серйозність інцидентів для кожної ситуації
        incident_severity = incidents_df.groupby('situation_id')['severity'].mean().reset_index(name='avg_severity')
        
        # Рахуємо кількість постраждалих
        casualties = incidents_df.groupby('situation_id')['casualties'].sum().reset_index(name='total_casualties')
        
        # Рахуємо кількість інцидентів з пошкодженням майна
        property_damage = incidents_df.groupby('situation_id')['property_damage'].sum().reset_index(name='property_damage_count')
        
        # Об'єднуємо дані про ситуації та інциденти
        df = situations_df.merge(incident_counts, left_on='id', right_on='situation_id', how='left')
        df = df.merge(incident_severity, left_on='id', right_on='situation_id', how='left')
        df = df.merge(casualties, left_on='id', right_on='situation_id', how='left')
        df = df.merge(property_damage, left_on='id', right_on='situation_id', how='left')
        
        # Додаємо дані про підрозділи
        df = df.merge(units_df[['id', 'unit_type', 'personnel_count', 'readiness_level']], 
                      left_on='unit_id', right_on='id', how='left', suffixes=('', '_unit'))
        
        # Заповнюємо пропущені значення
        df['readiness_level'] = df['readiness_level'].fillna(3)  # Середній рівень за замовчуванням
        df['personnel_count'] = df['personnel_count'].fillna(df['personnel_count'].median())
        df['unit_type'] = df['unit_type'].fillna('Оперативного призначення')  # Найпоширеніший тип за замовчуванням
        
        # Розраховуємо загальну кількість виділених ресурсів для кожної ситуації
        total_resources = allocations_df.groupby('situation_id')['quantity_allocated'].sum().reset_index(name='total_resources')
        df = df.merge(total_resources, left_on='id', right_on='situation_id', how='left')
        df['total_resources'] = df['total_resources'].fillna(0)
        
        # Заповнюємо пропущені значення для числових стовпців
        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                df[col] = df[col].fillna(0)
        
        # Вибираємо ознаки та цільову змінну
        features = [
            'threat_level', 
            'Порушення громадського порядку', 'Терористична загроза', 'Диверсія', 'Масові заворушення', 'Блокування об\'єктів',
            'avg_severity', 'total_casualties', 'property_damage_count',
            'readiness_level', 'personnel_count', 'region', 'location', 'status', 'unit_type'
        ]
        
        # Перевіряємо наявність всіх стовпців
        for feature in features:
            if feature not in df.columns:
                if feature in incident_types:
                    df[feature] = 0
                else:
                    print(f"Відсутня ознака: {feature}")
        
        X = df[features]
        y = df['total_resources']
        
        return X, y
        
    def train_resource_need_model(self):
        """Навчання моделі для прогнозування потреб у ресурсах для підрозділів НГУ"""
        X, y = self.prepare_resource_need_data()
        
        # Розділяємо дані на тренувальну та тестову вибірки
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Визначаємо числові та категоріальні ознаки
        numeric_features = [
            'threat_level', 
            'Порушення громадського порядку', 'Терористична загроза', 'Диверсія', 'Масові заворушення', 'Блокування об\'єктів',
            'avg_severity', 'total_casualties', 'property_damage_count',
            'readiness_level', 'personnel_count'
        ]
        categorical_features = ['region', 'location', 'status', 'unit_type']
        
        # Створюємо препроцесори для різних типів ознак
        numeric_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])
        
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        
        # Об'єднуємо препроцесори
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])
        
        # Створюємо пайплайн з препроцесором та моделлю
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
        ])
        
        # Навчаємо модель
        model.fit(X_train, y_train)
        
        # Оцінюємо модель
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        
        print(f"RMSE моделі прогнозування потреб у ресурсах: {rmse:.4f}")
        
        # Зберігаємо модель під двома назвами для сумісності з analytics_ai.py
        self.models['resource_need'] = model
        self.models['resource_predictor'] = model  # Додаємо другу назву для сумісності
        
        return model, rmse
        
    def predict_resource_need(self, threat_level, region, location, status, unit_type, personnel_count, readiness_level=3, incident_types=None, avg_severity=0, total_casualties=0, property_damage_count=0):
        """Прогнозування потреб у ресурсах для підрозділів НГУ"""
        if 'resource_need' not in self.models and 'resource_predictor' not in self.models:
            self.train_resource_need_model()
        
        # Поточний час
        now = datetime.datetime.now()
        
        # Якщо не передано дані про типи інцидентів, ініціалізуємо порожнім словником
        if incident_types is None:
            incident_types = {
                'Порушення громадського порядку': 0,
                'Терористична загроза': 0,
                'Диверсія': 0,
                'Масові заворушення': 0,
                'Блокування об\'єктів': 0
            }
        
        # Створюємо DataFrame з вхідними даними
        data = {
            'threat_level': [threat_level],
            'avg_severity': [avg_severity],
            'total_casualties': [total_casualties],
            'property_damage_count': [property_damage_count],
            'readiness_level': [readiness_level],
            'personnel_count': [personnel_count],
            'region': [region],
            'location': [location],
            'status': [status],
            'unit_type': [unit_type]
        }
        
        # Додаємо дані про типи інцидентів
        for incident_type, count in incident_types.items():
            data[incident_type] = [count]
        
        df = pd.DataFrame(data)
        
        # Прогнозуємо потреби у ресурсах
        predicted_resources = self.models['resource_need'].predict(df)[0]
        
        # Розраховуємо розподіл ресурсів за типами (приблизно)
        resource_distribution = {
            'Особовий склад': int(predicted_resources * 0.5),  # 50% ресурсів - особовий склад
            'Техніка': int(predicted_resources * 0.2),        # 20% ресурсів - техніка
            'Озброєння': int(predicted_resources * 0.15),     # 15% ресурсів - озброєння
            'Боєприпаси': int(predicted_resources * 0.1),     # 10% ресурсів - боєприпаси
            'Спорядження': int(predicted_resources * 0.05)    # 5% ресурсів - спорядження
        }
        
        # Зберігаємо прогноз у базі даних
        prediction = Prediction(
            timestamp=now,
            prediction_type='Ресурси',
            location=location,
            region=region,
            prediction_value=float(predicted_resources),
            confidence=0.8,  # Можна розрахувати більш точно
            description=f"Прогноз потреб у ресурсах для підрозділу НГУ типу {unit_type} в {region} ({location}) з рівнем загрози {threat_level}",
            resource_type='Загальні потреби'
        )
        self.session.add(prediction)
        self.session.commit()
        
        return {
            'predicted_resources': predicted_resources,
            'resource_distribution': resource_distribution,
            'prediction_id': prediction.id
        }
    
    def analyze_incident_trends(self, days=30):
        """Аналіз трендів інцидентів за останній період"""
        # Отримуємо дані про інциденти за останній період
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
        query = self.session.query(Incident).filter(Incident.timestamp >= cutoff_date).order_by(Incident.timestamp)
        incidents_df = pd.read_sql(query.statement, self.engine)
        
        if incidents_df.empty:
            return {
                'status': 'error',
                'message': 'Недостатньо даних для аналізу трендів'
            }
        
        # Додаємо часові ознаки
        incidents_df['date'] = incidents_df['timestamp'].dt.date
        
        # Рахуємо кількість інцидентів за день
        daily_incidents = incidents_df.groupby(['date', 'type']).size().reset_index(name='count')
        
        # Рахуємо середню серйозність інцидентів за день
        daily_severity = incidents_df.groupby(['date', 'type'])['severity'].mean().reset_index(name='avg_severity')
        
        # Об'єднуємо дані
        trends_df = daily_incidents.merge(daily_severity, on=['date', 'type'])
        
        # Аналізуємо тренди
        trends = {}
        for incident_type in trends_df['type'].unique():
            type_data = trends_df[trends_df['type'] == incident_type]
            
            # Розраховуємо зміну кількості інцидентів
            count_change = type_data['count'].pct_change().mean() * 100
            
            # Розраховуємо зміну серйозності інцидентів
            severity_change = type_data['avg_severity'].pct_change().mean() * 100
            
            trends[incident_type] = {
                'count_change': count_change,
                'severity_change': severity_change,
                'avg_daily_count': type_data['count'].mean(),
                'avg_severity': type_data['avg_severity'].mean(),
                'data': type_data.to_dict('records')
            }
        
        return {
            'status': 'success',
            'trends': trends,
            'period_days': days
        }
    
    def evaluate_decision_effectiveness(self, days=30):
        """Оцінка ефективності прийнятих рішень"""
        # Отримуємо дані про рішення за останній період
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
        decisions_df = pd.read_sql(
            self.session.query(Decision).filter(Decision.decision_time >= cutoff_date).statement,
            self.engine
        )
        
        if decisions_df.empty:
            return {
                'status': 'error',
                'message': 'Недостатньо даних для оцінки ефективності рішень'
            }
        
        # Отримуємо дані про ситуації
        situations_df = self.get_situation_data()
        
        # Об'єднуємо дані
        df = decisions_df.merge(
            situations_df,
            left_on='situation_id',
            right_on='id',
            suffixes=('_decision', '_situation')
        )
        
        # Розраховуємо метрики ефективності
        effectiveness = {
            'avg_effectiveness': df['effectiveness_score'].mean(),
            'high_effectiveness_count': (df['effectiveness_score'] >= 8).sum(),
            'medium_effectiveness_count': ((df['effectiveness_score'] >= 5) & (df['effectiveness_score'] < 8)).sum(),
            'low_effectiveness_count': (df['effectiveness_score'] < 5).sum(),
            'by_decision_type': {}
        }
        
        # Розраховуємо ефективність за типами рішень
        for decision_type in df['decision_type'].unique():
            type_data = df[df['decision_type'] == decision_type]
            effectiveness['by_decision_type'][decision_type] = {
                'avg_effectiveness': type_data['effectiveness_score'].mean(),
                'count': len(type_data),
                'avg_implementation_time': (type_data['implementation_time'] - type_data['decision_time']).mean().total_seconds() / 60  # в хвилинах
            }
        
        return {
            'status': 'success',
            'effectiveness': effectiveness,
            'period_days': days
        }
    
    def save_models(self, directory=None):
        """Збереження моделей на диск"""
        # Використовуємо директорію за замовчуванням, якщо не вказано іншу
        if directory is None:
            directory = self.models_dir
            
        # Отримуємо шлях до директорії моделей з конфігурації, якщо можливо
        try:
            from config.config import MODELS_DIR, ANALYTICS_CONFIG
            # Спочатку перевіряємо, чи є альтернативний шлях у конфігурації аналітики
            if 'models_dir' in ANALYTICS_CONFIG:
                directory = ANALYTICS_CONFIG['models_dir']
                print(f"Використовуємо шлях до моделей з ANALYTICS_CONFIG: {directory}")
            else:
                directory = MODELS_DIR
                print(f"Використовуємо стандартний шлях до моделей з конфігурації: {directory}")
        except (ImportError, KeyError) as e:
            print(f"Використовуємо стандартну директорію моделей: {directory}. Помилка: {e}")
            
        # Перевіряємо, чи є шлях абсолютним, якщо ні - перетворюємо його
        if not os.path.isabs(directory):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            directory = os.path.join(base_dir, directory)
            print(f"Перетворено відносний шлях на абсолютний: {directory}")
            
        # Створюємо директорію, якщо вона не існує
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"Директорія {directory} перевірена/створена успішно")
        except Exception as e:
            print(f"Помилка при створенні директорії {directory}: {e}")
            return False
        
        # Зберігаємо шлях до директорії моделей для подальшого використання
        self.models_dir = directory
        
        # Зберігаємо кожну модель
        models_saved = 0
        for model_name, model in self.models.items():
            # Пропускаємо дублікат моделі resource_predictor, якщо вона ідентична resource_need
            if model_name == 'resource_predictor' and 'resource_need' in self.models and id(self.models['resource_predictor']) == id(self.models['resource_need']):
                print(f"Модель {model_name} є дублікатом resource_need, використовуємо один файл")
                continue
                
            model_path = os.path.join(directory, f"{model_name}.joblib")
            try:
                # Створюємо резервну копію існуючої моделі, якщо вона є
                if os.path.exists(model_path):
                    backup_path = os.path.join(directory, f"{model_name}.joblib.bak")
                    try:
                        import shutil
                        shutil.copy2(model_path, backup_path)
                        print(f"Створено резервну копію моделі {model_name}")
                    except Exception as e:
                        print(f"Не вдалося створити резервну копію моделі {model_name}: {e}")
                
                # Зберігаємо модель
                joblib.dump(model, model_path)
                print(f"Модель {model_name} збережена у {model_path}")
                models_saved += 1
                
                # Якщо це модель resource_need, також зберігаємо її як resource_predictor для сумісності
                if model_name == 'resource_need' and 'resource_predictor' not in self.models:
                    predictor_path = os.path.join(directory, "resource_predictor.joblib")
                    joblib.dump(model, predictor_path)
                    print(f"Модель resource_need також збережена як resource_predictor для сумісності")
                    models_saved += 1
            except Exception as e:
                print(f"Помилка збереження моделі {model_name}: {e}")
                # Відновлюємо з резервної копії, якщо вона є
                backup_path = os.path.join(directory, f"{model_name}.joblib.bak")
                if os.path.exists(backup_path):
                    try:
                        import shutil
                        shutil.copy2(backup_path, model_path)
                        print(f"Відновлено модель {model_name} з резервної копії")
                    except Exception as backup_error:
                        print(f"Не вдалося відновити модель з резервної копії: {backup_error}")
        
        print(f"Збережено {models_saved} моделей")
        return models_saved > 0
    
    def load_models(self, directory=None):
        """Завантаження моделей з диску"""
        # Використовуємо директорію за замовчуванням, якщо не вказано іншу
        if directory is None:
            directory = self.models_dir
            
        # Отримуємо шлях до директорії моделей з конфігурації
        try:
            from config.config import MODELS_DIR, ANALYTICS_CONFIG
            # Спочатку перевіряємо, чи є альтернативний шлях у конфігурації аналітики
            if 'models_dir' in ANALYTICS_CONFIG:
                directory = ANALYTICS_CONFIG['models_dir']
                print(f"Використовуємо шлях до моделей з ANALYTICS_CONFIG: {directory}")
            else:
                directory = MODELS_DIR
                print(f"Використовуємо стандартний шлях до моделей з конфігурації: {directory}")
        except (ImportError, KeyError) as e:
            print(f"Використовуємо стандартну директорію моделей: {directory}. Помилка: {e}")
            
        # Перевіряємо, чи є шлях абсолютним, якщо ні - перетворюємо його
        if not os.path.isabs(directory):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            directory = os.path.join(base_dir, directory)
            print(f"Перетворено відносний шлях на абсолютний: {directory}")
            
        # Перевіряємо, чи існує директорія, і створюємо її за потреби
        if not os.path.exists(directory):
            print(f"Директорія {directory} не існує. Спроба створити...")
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"Директорія {directory} успішно створена")
            except Exception as e:
                print(f"Не вдалося створити директорію {directory}: {e}")
                self.initialize_empty_models()
                return False
        
        # Перевіряємо, чи є файли моделей у директорії
        try:
            model_files = [f for f in os.listdir(directory) if f.endswith('.joblib')]
            if not model_files:
                print(f"У директорії {directory} не знайдено файлів моделей (.joblib)")
                print("Моделі будуть створені при першому використанні відповідних функції.")
                self.initialize_empty_models()
                return False
        except Exception as e:
            print(f"Помилка при скануванні директорії {directory}: {e}")
            self.initialize_empty_models()
            return False
        
        # Зберігаємо шлях до директорії моделей для подальшого використання
        self.models_dir = directory
        
        # Завантажуємо кожну модель
        models_loaded = 0
        resource_model = None
        
        # Визначаємо стандартні моделі, які повинні бути завантажені
        standard_models = {
            'threat_predictor': 'Прогнозування рівня загрози',
            'resource_predictor': 'Прогнозування потреб у ресурсах',
            'incident_predictor': 'Прогнозування інцидентів',
            'resource_need': 'Прогнозування потреб у ресурсах (альтернативна назва)',
            'threat_prediction': 'Прогнозування рівня загрози (альтернативна назва)'
        }
        
        # Перевіряємо наявність файлів моделей
        model_files = {}
        for model_name in standard_models.keys():
            model_path = os.path.join(directory, f"{model_name}.joblib")
            if os.path.exists(model_path):
                model_files[model_name] = model_path
            else:
                print(f"Файл моделі {model_name}.joblib не знайдено в {directory}")
        
        # Спочатку перевіряємо, чи є файл resource_need.joblib
        resource_need_path = os.path.join(directory, "resource_need.joblib")
        resource_predictor_path = os.path.join(directory, "resource_predictor.joblib")
        
        # Завантажуємо resource_need, якщо він існує
        if os.path.exists(resource_need_path):
            try:
                resource_model = joblib.load(resource_need_path)
                self.models['resource_need'] = resource_model
                print(f"Модель resource_need завантажена з {resource_need_path}")
                models_loaded += 1
            except Exception as e:
                print(f"Помилка завантаження моделі resource_need: {e}")
                print(f"Спробуйте перенавчити модель або перевірити цілісність файлу")
        
        # Завантажуємо resource_predictor, якщо він існує
        if os.path.exists(resource_predictor_path):
            try:
                # Перевіряємо, чи це не той самий файл, що й resource_need (для уникнення дублювання)
                if resource_model is not None and os.path.exists(resource_need_path):
                    try:
                        if os.path.samefile(resource_need_path, resource_predictor_path):
                            self.models['resource_predictor'] = resource_model
                            print(f"Модель resource_predictor є тим самим файлом, що й resource_need")
                        else:
                            # Завантажуємо окрему модель resource_predictor
                            resource_predictor_model = joblib.load(resource_predictor_path)
                            self.models['resource_predictor'] = resource_predictor_model
                            print(f"Модель resource_predictor завантажена з {resource_predictor_path}")
                            models_loaded += 1
                    except OSError:
                        # Якщо не вдалося порівняти файли, завантажуємо окремо
                        resource_predictor_model = joblib.load(resource_predictor_path)
                        self.models['resource_predictor'] = resource_predictor_model
                        print(f"Модель resource_predictor завантажена з {resource_predictor_path}")
                        models_loaded += 1
                else:
                    # Завантажуємо окрему модель resource_predictor
                    resource_predictor_model = joblib.load(resource_predictor_path)
                    self.models['resource_predictor'] = resource_predictor_model
                    print(f"Модель resource_predictor завантажена з {resource_predictor_path}")
                    models_loaded += 1
                    
                # Якщо resource_need не був завантажений, використовуємо resource_predictor для сумісності
                if resource_model is None:
                    self.models['resource_need'] = self.models['resource_predictor']
                    print(f"Використовуємо resource_predictor як resource_need для сумісності")
            except Exception as e:
                print(f"Помилка завантаження моделі resource_predictor: {e}")
                print(f"Спробуйте перенавчити модель або перевірити цілісність файлу")
                # Використовуємо resource_need як запасний варіант, якщо він був завантажений
                if resource_model is not None:
                    self.models['resource_predictor'] = resource_model
                    print(f"Використовуємо resource_need як resource_predictor для сумісності")
        elif resource_model is not None:
            # Якщо resource_predictor не існує, але resource_need був завантажений, використовуємо його
            self.models['resource_predictor'] = resource_model
            print(f"Використовуємо resource_need як resource_predictor для сумісності")
        
        # Завантажуємо threat_predictor, якщо він існує
        threat_predictor_path = os.path.join(directory, "threat_predictor.joblib")
        if os.path.exists(threat_predictor_path):
            try:
                self.models['threat_predictor'] = joblib.load(threat_predictor_path)
                print(f"Модель threat_predictor завантажена з {threat_predictor_path}")
                models_loaded += 1
            except Exception as e:
                print(f"Помилка завантаження моделі threat_predictor: {e}")
                print(f"Спробуйте перенавчити модель або перевірити цілісність файлу")
        
        # Завантажуємо incident_predictor, якщо він існує
        incident_predictor_path = os.path.join(directory, "incident_predictor.joblib")
        if os.path.exists(incident_predictor_path):
            try:
                self.models['incident_predictor'] = joblib.load(incident_predictor_path)
                print(f"Модель incident_predictor завантажена з {incident_predictor_path}")
                models_loaded += 1
            except Exception as e:
                print(f"Помилка завантаження моделі incident_predictor: {e}")
                print(f"Спробуйте перенавчити модель або перевірити цілісність файлу")
        
        # Завантажуємо інші моделі, які не були завантажені вище
        try:
            for model_file in os.listdir(directory):
                if model_file.endswith('.joblib'):
                    model_name = os.path.splitext(model_file)[0]
                    # Пропускаємо вже завантажені моделі
                    if model_name in self.models or model_name in ['resource_need', 'resource_predictor', 'threat_predictor', 'incident_predictor']:
                        continue
                        
                    model_path = os.path.join(directory, model_file)
                    try:
                        self.models[model_name] = joblib.load(model_path)
                        print(f"Модель {model_name} завантажена з {model_path}")
                        models_loaded += 1
                    except Exception as e:
                        print(f"Помилка завантаження моделі {model_name}: {e}")
                        print(f"Спробуйте перенавчити модель або перевірити цілісність файлу")
        except Exception as e:
            print(f"Помилка при скануванні директорії моделей: {e}")
        
        # Перевіряємо, чи всі стандартні моделі завантажені
        missing_models = [name for name in standard_models.keys() if name not in self.models and name != 'resource_need']
        if missing_models:
            print(f"Увага: Не знайдено наступні стандартні моделі: {', '.join(missing_models)}")
            print("Система може працювати некоректно без цих моделей.")
            print("Рекомендується запустити навчання моделей через відповідні функції.")
        
        # Додаємо альтернативну назву для threat_predictor, якщо вона завантажена
        if 'threat_predictor' in self.models and 'threat_prediction' not in self.models:
            self.models['threat_prediction'] = self.models['threat_predictor']
            print("Додано альтернативну назву 'threat_prediction' для моделі 'threat_predictor'")
        
        if models_loaded > 0:
            print(f"Завантажено {models_loaded} моделей")
        else:
            print("Не знайдено жодної моделі для завантаження")
            print("Моделі будуть створені при першому використанні відповідних функцій.")
            self.initialize_empty_models()
            
        return models_loaded > 0

    def initialize_empty_models(self):
        """Ініціалізація порожніх моделей для уникнення помилок"""
        print("Ініціалізація порожніх моделей для уникнення помилок...")
        try:
            # Створюємо прості моделі-заглушки
            from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
            
            # Модель для прогнозування загроз (класифікація)
            self.models['threat_predictor'] = RandomForestClassifier(n_estimators=10)
            self.models['threat_prediction'] = self.models['threat_predictor']  # Альтернативна назва
            
            # Моделі для прогнозування ресурсів (регресія)
            resource_model = RandomForestRegressor(n_estimators=10)
            self.models['resource_predictor'] = resource_model
            self.models['resource_need'] = resource_model
            
            # Модель для прогнозування інцидентів (класифікація)
            self.models['incident_predictor'] = RandomForestClassifier(n_estimators=10)
            
            print("Порожні моделі успішно ініціалізовані")
            return True
        except Exception as e:
            print(f"Помилка при ініціалізації порожніх моделей: {e}")
            return False

# Приклад використання
if __name__ == "__main__":
    analytics = NGUAnalytics()
    
    # Навчання моделей
    threat_model, accuracy, report = analytics.train_threat_prediction_model()
    resource_model, rmse = analytics.train_resource_need_model()
    
    # Прогнозування
    resource_prediction = analytics.predict_resource_need(
        threat_level=4, 
        region="Схід", 
        location="Напружена", 
        status="Критична", 
        unit_type="Оперативного призначення", 
        personnel_count=100, 
        avg_severity=4
    )
    
    # Аналіз трендів
    trends = analytics.analyze_incident_trends(days=30)
    
    # Оцінка ефективності рішень
    effectiveness = analytics.evaluate_decision_effectiveness(days=30)
    
    # Зберігання моделей
    analytics.save_models()