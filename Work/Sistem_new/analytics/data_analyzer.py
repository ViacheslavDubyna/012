#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль для аналізу даних та підготовки їх для машинного навчання.
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import psycopg2
import logging
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('data_analyzer')

# Параметри підключення до бази даних
DB_PARAMS = {
    'dbname': 'ngu_decision_support',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'client_encoding': 'utf-8'
}

# Клас для аналізу даних
class DataAnalyzer:
    def __init__(self, db_params=DB_PARAMS):
        self.db_params = db_params
        self.conn = None
        self.cursor = None
    
    def connect_to_db(self):
        """
        Підключення до бази даних
        """
        try:
            self.conn = psycopg2.connect(**self.db_params)
            self.cursor = self.conn.cursor()
            logger.info("Успішне підключення до бази даних")
            return True
        except Exception as e:
            logger.error(f"Помилка підключення до бази даних: {e}")
            return False
    
    def disconnect_from_db(self):
        """
        Відключення від бази даних
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("Відключення від бази даних")
    
    def get_operational_data(self, days=30):
        """
        Отримання оперативних даних за останні N днів
        """
        try:
            query = """
                SELECT id, timestamp, location, description, threat_level, created_at, updated_at
                FROM operational_situation
                WHERE timestamp >= %s
                ORDER BY timestamp DESC
            """
            
            start_date = datetime.now() - timedelta(days=days)
            self.cursor.execute(query, (start_date,))
            columns = [desc[0] for desc in self.cursor.description]
            data = self.cursor.fetchall()
            
            df = pd.DataFrame(data, columns=columns)
            logger.info(f"Отримано {len(df)} записів оперативних даних за останні {days} днів")
            return df
        except Exception as e:
            logger.error(f"Помилка при отриманні оперативних даних: {e}")
            return pd.DataFrame()
    
    def get_incident_data(self, days=30):
        """
        Отримання даних про інциденти за останні N днів
        """
        try:
            query = """
                SELECT id, timestamp, location, incident_type, description, casualties, wounded, created_at, updated_at
                FROM incidents
                WHERE timestamp >= %s
                ORDER BY timestamp DESC
            """
            
            start_date = datetime.now() - timedelta(days=days)
            self.cursor.execute(query, (start_date,))
            columns = [desc[0] for desc in self.cursor.description]
            data = self.cursor.fetchall()
            
            df = pd.DataFrame(data, columns=columns)
            logger.info(f"Отримано {len(df)} записів про інциденти за останні {days} днів")
            return df
        except Exception as e:
            logger.error(f"Помилка при отриманні даних про інциденти: {e}")
            return pd.DataFrame()
    
    def get_personnel_data(self, days=30):
        """
        Отримання даних про особовий склад за останні N днів
        """
        try:
            query = """
                SELECT p.id, p.rank, p.last_name, p.first_name, p.patronymic, p.unit, p.status, 
                       p.incident_id, p.injury_description, p.created_at, p.updated_at, i.timestamp
                FROM personnel p
                JOIN incidents i ON p.incident_id = i.id
                WHERE i.timestamp >= %s
                ORDER BY i.timestamp DESC
            """
            
            start_date = datetime.now() - timedelta(days=days)
            self.cursor.execute(query, (start_date,))
            columns = [desc[0] for desc in self.cursor.description]
            data = self.cursor.fetchall()
            
            df = pd.DataFrame(data, columns=columns)
            logger.info(f"Отримано {len(df)} записів про особовий склад за останні {days} днів")
            return df
        except Exception as e:
            logger.error(f"Помилка при отриманні даних про особовий склад: {e}")
            return pd.DataFrame()
    
    def get_decisions_data(self, days=30):
        """
        Отримання даних про прийняті рішення за останні N днів
        """
        try:
            query = """
                SELECT id, timestamp, decision_maker, description, action_taken, result, effectiveness, created_at, updated_at
                FROM decisions
                WHERE timestamp >= %s
                ORDER BY timestamp DESC
            """
            
            start_date = datetime.now() - timedelta(days=days)
            self.cursor.execute(query, (start_date,))
            columns = [desc[0] for desc in self.cursor.description]
            data = self.cursor.fetchall()
            
            df = pd.DataFrame(data, columns=columns)
            logger.info(f"Отримано {len(df)} записів про прийняті рішення за останні {days} днів")
            return df
        except Exception as e:
            logger.error(f"Помилка при отриманні даних про прийняті рішення: {e}")
            return pd.DataFrame()
    
    def prepare_data_for_analysis(self, days=30):
        """
        Підготовка даних для аналізу
        """
        if not self.connect_to_db():
            return None
        
        try:
            # Отримання даних з бази
            operational_df = self.get_operational_data(days)
            incident_df = self.get_incident_data(days)
            personnel_df = self.get_personnel_data(days)
            decisions_df = self.get_decisions_data(days)
            
            # Перевірка наявності даних
            if operational_df.empty or incident_df.empty:
                logger.warning("Недостатньо даних для аналізу")
                return None
            
            # Агрегація даних про інциденти за локацією та датою
            incident_df['date'] = incident_df['timestamp'].dt.date
            incident_agg = incident_df.groupby(['location', 'date']).agg({
                'casualties': 'sum',
                'wounded': 'sum',
                'id': 'count'
            }).reset_index()
            incident_agg.rename(columns={'id': 'incident_count'}, inplace=True)
            
            # Агрегація оперативних даних за локацією та датою
            operational_df['date'] = operational_df['timestamp'].dt.date
            operational_agg = operational_df.groupby(['location', 'date']).agg({
                'threat_level': 'mean'
            }).reset_index()
            
            # Об'єднання даних
            merged_df = pd.merge(
                incident_agg,
                operational_agg,
                on=['location', 'date'],
                how='outer'
            )
            
            # Заповнення пропущених значень
            merged_df['incident_count'] = merged_df['incident_count'].fillna(0)
            merged_df['casualties'] = merged_df['casualties'].fillna(0)
            merged_df['wounded'] = merged_df['wounded'].fillna(0)
            merged_df['threat_level'] = merged_df['threat_level'].fillna(merged_df['threat_level'].mean())
            
            # Додавання часових ознак
            merged_df['day_of_week'] = pd.to_datetime(merged_df['date']).dt.dayofweek
            merged_df['month'] = pd.to_datetime(merged_df['date']).dt.month
            
            # Додавання лагових ознак (дані за попередні дні)
            for location in merged_df['location'].unique():
                location_df = merged_df[merged_df['location'] == location].sort_values('date')
                
                for lag in range(1, 4):  # Лаги на 1, 2 і 3 дні
                    merged_df.loc[merged_df['location'] == location, f'threat_level_lag_{lag}'] = \
                        location_df['threat_level'].shift(lag)
                    merged_df.loc[merged_df['location'] == location, f'incident_count_lag_{lag}'] = \
                        location_df['incident_count'].shift(lag)
                    merged_df.loc[merged_df['location'] == location, f'casualties_lag_{lag}'] = \
                        location_df['casualties'].shift(lag)
                    merged_df.loc[merged_df['location'] == location, f'wounded_lag_{lag}'] = \
                        location_df['wounded'].shift(lag)
            
            # Заповнення пропущених значень для лагових ознак
            lag_columns = [col for col in merged_df.columns if 'lag' in col]
            for col in lag_columns:
                merged_df[col] = merged_df[col].fillna(0)
            
            logger.info(f"Підготовлено {len(merged_df)} записів для аналізу")
            return merged_df
        except Exception as e:
            logger.error(f"Помилка при підготовці даних для аналізу: {e}")
            return None
        finally:
            self.disconnect_from_db()
    
    def create_feature_pipeline(self, categorical_features, numerical_features):
        """
        Створення пайплайну для обробки ознак
        """
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        
        numerical_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', categorical_transformer, categorical_features),
                ('num', numerical_transformer, numerical_features)
            ])
        
        return preprocessor
    
    def analyze_casualties_by_location(self, days=30):
        """
        Аналіз втрат за локаціями
        """
        if not self.connect_to_db():
            return None
        
        try:
            # Отримання даних про інциденти
            incident_df = self.get_incident_data(days)
            
            if incident_df.empty:
                logger.warning("Немає даних про інциденти для аналізу")
                return None
            
            # Агрегація даних за локацією
            location_stats = incident_df.groupby('location').agg({
                'casualties': 'sum',
                'wounded': 'sum',
                'id': 'count'
            }).reset_index()
            location_stats.rename(columns={'id': 'incident_count'}, inplace=True)
            location_stats['total_casualties'] = location_stats['casualties'] + location_stats['wounded']
            location_stats.sort_values('total_casualties', ascending=False, inplace=True)
            
            logger.info(f"Проаналізовано втрати за {len(location_stats)} локаціями")
            return location_stats
        except Exception as e:
            logger.error(f"Помилка при аналізі втрат за локаціями: {e}")
            return None
        finally:
            self.disconnect_from_db()
    
    def analyze_casualties_by_time(self, days=30, interval='day'):
        """
        Аналіз втрат за часом
        """
        if not self.connect_to_db():
            return None
        
        try:
            # Отримання даних про інциденти
            incident_df = self.get_incident_data(days)
            
            if incident_df.empty:
                logger.warning("Немає даних про інциденти для аналізу")
                return None
            
            # Додавання часових ознак
            if interval == 'day':
                incident_df['time_group'] = incident_df['timestamp'].dt.date
            elif interval == 'week':
                incident_df['time_group'] = incident_df['timestamp'].dt.isocalendar().week
            elif interval == 'month':
                incident_df['time_group'] = incident_df['timestamp'].dt.month
            elif interval == 'hour':
                incident_df['time_group'] = incident_df['timestamp'].dt.hour
            else:
                incident_df['time_group'] = incident_df['timestamp'].dt.date
            
            # Агрегація даних за часовим інтервалом
            time_stats = incident_df.groupby('time_group').agg({
                'casualties': 'sum',
                'wounded': 'sum',
                'id': 'count'
            }).reset_index()
            time_stats.rename(columns={'id': 'incident_count'}, inplace=True)
            time_stats['total_casualties'] = time_stats['casualties'] + time_stats['wounded']
            time_stats.sort_values('time_group', inplace=True)
            
            logger.info(f"Проаналізовано втрати за {len(time_stats)} часовими інтервалами")
            return time_stats
        except Exception as e:
            logger.error(f"Помилка при аналізі втрат за часом: {e}")
            return None
        finally:
            self.disconnect_from_db()
    
    def analyze_incident_types(self, days=30):
        """
        Аналіз типів інцидентів
        """
        if not self.connect_to_db():
            return None
        
        try:
            # Отримання даних про інциденти
            incident_df = self.get_incident_data(days)
            
            if incident_df.empty:
                logger.warning("Немає даних про інциденти для аналізу")
                return None
            
            # Агрегація даних за типом інциденту
            type_stats = incident_df.groupby('incident_type').agg({
                'casualties': 'sum',
                'wounded': 'sum',
                'id': 'count'
            }).reset_index()
            type_stats.rename(columns={'id': 'incident_count'}, inplace=True)
            type_stats['total_casualties'] = type_stats['casualties'] + type_stats['wounded']
            type_stats.sort_values('total_casualties', ascending=False, inplace=True)
            
            logger.info(f"Проаналізовано {len(type_stats)} типів інцидентів")
            return type_stats
        except Exception as e:
            logger.error(f"Помилка при аналізі типів інцидентів: {e}")
            return None
        finally:
            self.disconnect_from_db()
    
    def analyze_unit_casualties(self, days=30):
        """
        Аналіз втрат за підрозділами
        """
        if not self.connect_to_db():
            return None
        
        try:
            # Отримання даних про особовий склад
            personnel_df = self.get_personnel_data(days)
            
            if personnel_df.empty:
                logger.warning("Немає даних про особовий склад для аналізу")
                return None
            
            # Агрегація даних за підрозділом
            unit_stats = personnel_df.groupby('unit').agg({
                'id': 'count',
                'status': lambda x: (x == 'killed').sum()
            }).reset_index()
            unit_stats.rename(columns={'id': 'total', 'status': 'killed'}, inplace=True)
            unit_stats['wounded'] = unit_stats['total'] - unit_stats['killed']
            unit_stats.sort_values('total', ascending=False, inplace=True)
            
            logger.info(f"Проаналізовано втрати за {len(unit_stats)} підрозділами")
            return unit_stats
        except Exception as e:
            logger.error(f"Помилка при аналізі втрат за підрозділами: {e}")
            return None
        finally:
            self.disconnect_from_db()

# Функція для запуску аналізу даних
def run_data_analysis(days=30):
    analyzer = DataAnalyzer()
    
    # Підготовка даних для аналізу
    data = analyzer.prepare_data_for_analysis(days)
    
    # Аналіз втрат за локаціями
    location_stats = analyzer.analyze_casualties_by_location(days)
    
    # Аналіз втрат за часом
    time_stats = analyzer.analyze_casualties_by_time(days)
    
    # Аналіз типів інцидентів
    type_stats = analyzer.analyze_incident_types(days)
    
    # Аналіз втрат за підрозділами
    unit_stats = analyzer.analyze_unit_casualties(days)
    
    return {
        'data': data,
        'location_stats': location_stats,
        'time_stats': time_stats,
        'type_stats': type_stats,
        'unit_stats': unit_stats
    }

# Головна функція
def main():
    logger.info("Запуск модуля аналізу даних...")
    
    # Запуск аналізу даних за останні 30 днів
    results = run_data_analysis(30)
    
    if results['data'] is not None:
        logger.info("Модуль аналізу даних успішно завершив роботу")
    else:
        logger.error("Модуль аналізу даних завершив роботу з помилками")

if __name__ == "__main__":
    main()