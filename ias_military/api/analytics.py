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

# Конфігурація бази даних
DB_URL = "postgresql://postgres:postgres@localhost:5432/ngu_ias"

class NGUAnalytics:
    def __init__(self, db_url=DB_URL, models_dir='models'):
        self.engine = create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.models = {}
        self.models_dir = models_dir
        # Спробуємо завантажити збережені моделі при ініціалізації
        self.load_models(models_dir)
    
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
        
        # Зберігаємо модель
        self.models['resource_need'] = model
        
        return model, rmse
        
    def predict_resource_need(self, threat_level, region, location, status, unit_type, personnel_count, readiness_level=3, incident_types=None, avg_severity=0, total_casualties=0, property_damage_count=0):
        """Прогнозування потреб у ресурсах для підрозділів НГУ"""
        if 'resource_need' not in self.models:
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
            
        # Імпортуємо шлях до директорії моделей з конфігурації, якщо можливо
        try:
            from config.config import MODELS_DIR
            directory = MODELS_DIR
        except ImportError:
            pass
            
        # Створюємо директорію, якщо вона не існує
        os.makedirs(directory, exist_ok=True)
        
        # Зберігаємо кожну модель
        for model_name, model in self.models.items():
            model_path = os.path.join(directory, f"{model_name}.joblib")
            joblib.dump(model, model_path)
            print(f"Модель {model_name} збережена у {model_path}")
        
        return True
    
    def load_models(self, directory=None):
        """Завантаження моделей з диску"""
        # Використовуємо директорію за замовчуванням, якщо не вказано іншу
        if directory is None:
            directory = self.models_dir
            
        # Імпортуємо шлях до директорії моделей з конфігурації, якщо можливо
        try:
            from config.config import MODELS_DIR
            directory = MODELS_DIR
        except ImportError:
            pass
            
        # Перевіряємо, чи існує директорія
        if not os.path.exists(directory):
            print(f"Директорія {directory} не існує")
            return False
        
        # Завантажуємо кожну модель
        models_loaded = 0
        for model_file in os.listdir(directory):
            if model_file.endswith('.joblib'):
                model_name = os.path.splitext(model_file)[0]
                model_path = os.path.join(directory, model_file)
                try:
                    self.models[model_name] = joblib.load(model_path)
                    print(f"Модель {model_name} завантажена з {model_path}")
                    models_loaded += 1
                except Exception as e:
                    print(f"Помилка завантаження моделі {model_name}: {e}")
        
        if models_loaded > 0:
            print(f"Завантажено {models_loaded} моделей")
        else:
            print("Не знайдено жодної моделі для завантаження")
            
        return models_loaded > 0

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