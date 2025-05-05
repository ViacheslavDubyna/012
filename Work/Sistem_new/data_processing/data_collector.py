#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль для збору та попередньої обробки даних.
Імітує отримання даних з різних джерел та їх обробку перед збереженням у базу даних.
"""

import os
import sys
import json
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import psycopg2
from psycopg2 import sql
import logging

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('data_collector')

# Параметри підключення до бази даних
DB_PARAMS = {
    'dbname': 'ngu_decision_support',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'client_encoding': 'UTF8'
}

# Клас для збору даних
class DataCollector:
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
    
    def collect_operational_data(self):
        """
        Імітація збору оперативних даних з різних джерел
        """
        logger.info("Збір оперативних даних...")
        
        # Імітація даних з різних джерел
        locations = ['Харків', 'Донецьк', 'Луганськ', 'Запоріжжя', 'Херсон', 'Миколаїв', 'Суми', 'Чернігів']
        descriptions = [
            'Активні бойові дії', 'Артилерійські обстріли', 'Ракетні удари', 
            'Повітряна тривога', 'Диверсійна діяльність', 'Відносно спокійно'
        ]
        
        # Генерація випадкових даних
        now = datetime.now()
        data = []
        
        for _ in range(random.randint(3, 8)):  # Генеруємо від 3 до 8 нових записів
            timestamp = now - timedelta(hours=random.randint(0, 12))
            location = random.choice(locations)
            description = random.choice(descriptions)
            threat_level = random.randint(1, 5)
            
            data.append({
                'timestamp': timestamp,
                'location': location,
                'description': description,
                'threat_level': threat_level
            })
        
        return data
    
    def collect_incident_data(self):
        """
        Імітація збору даних про інциденти
        """
        logger.info("Збір даних про інциденти...")
        
        # Імітація даних про інциденти
        locations = ['Харків', 'Донецьк', 'Луганськ', 'Запоріжжя', 'Херсон', 'Миколаїв', 'Суми', 'Чернігів']
        incident_types = ['Артобстріл', 'Ракетний удар', 'Атака БПЛА', 'Мінометний обстріл', 'Снайперський вогонь']
        incident_descriptions = [
            'Масований обстріл позицій', 'Точковий удар по об\'єкту', 
            'Обстріл житлових районів', 'Атака на блокпост', 'Обстріл транспортного засобу'
        ]
        
        # Генерація випадкових даних
        now = datetime.now()
        data = []
        
        # Генеруємо від 0 до 3 нових інцидентів
        for _ in range(random.randint(0, 3)):
            timestamp = now - timedelta(hours=random.randint(0, 12))
            location = random.choice(locations)
            incident_type = random.choice(incident_types)
            description = random.choice(incident_descriptions)
            casualties = random.randint(0, 3)
            wounded = random.randint(0, 7)
            
            data.append({
                'timestamp': timestamp,
                'location': location,
                'incident_type': incident_type,
                'description': description,
                'casualties': casualties,
                'wounded': wounded
            })
        
        return data
    
    def collect_personnel_data(self, incident_id, casualties, wounded):
        """
        Імітація збору даних про постраждалий особовий склад
        """
        logger.info(f"Збір даних про постраждалий особовий склад для інциденту {incident_id}...")
        
        # Імітація даних про особовий склад
        ranks = ['солдат', 'старший солдат', 'молодший сержант', 'сержант', 'старший сержант', 
                 'старшина', 'прапорщик', 'старший прапорщик', 'молодший лейтенант', 'лейтенант', 
                 'старший лейтенант', 'капітан', 'майор', 'підполковник', 'полковник']
        last_names = ['Петренко', 'Іваненко', 'Коваленко', 'Бондаренко', 'Ткаченко', 'Шевченко', 
                      'Мельник', 'Кравченко', 'Бойко', 'Шевчук', 'Савченко', 'Руденко', 'Мороз']
        first_names = ['Іван', 'Петро', 'Олександр', 'Микола', 'Андрій', 'Сергій', 'Василь', 
                       'Юрій', 'Володимир', 'Віктор', 'Михайло', 'Дмитро', 'Олег']
        patronymics = ['Іванович', 'Петрович', 'Олександрович', 'Миколайович', 'Андрійович', 
                       'Сергійович', 'Васильович', 'Юрійович', 'Володимирович', 'Вікторович']
        units = ['1-й батальйон', '2-й батальйон', '3-й батальйон', 'Розвідрота', 'Штаб', 
                 'Медична рота', 'Інженерна рота', 'Рота зв\'язку', 'Артилерійський дивізіон']
        injury_descriptions = ['Осколкове поранення', 'Вогнепальне поранення', 'Контузія', 
                              'Множинні травми', 'Опіки', 'Ампутація кінцівки', 'Смерть']
        
        data = []
        
        # Генерація даних про загиблих
        for _ in range(casualties):
            rank = random.choice(ranks)
            last_name = random.choice(last_names)
            first_name = random.choice(first_names)
            patronymic = random.choice(patronymics)
            unit = random.choice(units)
            status = 'killed'
            
            data.append({
                'rank': rank,
                'last_name': last_name,
                'first_name': first_name,
                'patronymic': patronymic,
                'unit': unit,
                'status': status,
                'incident_id': incident_id,
                'injury_description': None
            })
        
        # Генерація даних про поранених
        for _ in range(wounded):
            rank = random.choice(ranks)
            last_name = random.choice(last_names)
            first_name = random.choice(first_names)
            patronymic = random.choice(patronymics)
            unit = random.choice(units)
            status = 'wounded'
            injury_description = random.choice(injury_descriptions)
            
            data.append({
                'rank': rank,
                'last_name': last_name,
                'first_name': first_name,
                'patronymic': patronymic,
                'unit': unit,
                'status': status,
                'incident_id': incident_id,
                'injury_description': injury_description
            })
        
        return data
    
    def preprocess_data(self, data, data_type):
        """
        Попередня обробка даних перед збереженням у базу даних
        """
        logger.info(f"Попередня обробка даних типу {data_type}...")
        
        if not data:
            return []
        
        # Перетворення даних у DataFrame для зручної обробки
        df = pd.DataFrame(data)
        
        if data_type == 'operational':
            # Обробка оперативних даних
            # Перевірка на дублікати
            df = df.drop_duplicates(subset=['timestamp', 'location'])
            
            # Нормалізація опису (видалення зайвих пробілів, приведення до нижнього регістру)
            df['description'] = df['description'].str.strip().str.lower()
            
            # Перевірка рівня загрози
            df['threat_level'] = df['threat_level'].clip(1, 5)
            
        elif data_type == 'incident':
            # Обробка даних про інциденти
            # Перевірка на дублікати
            df = df.drop_duplicates(subset=['timestamp', 'location', 'incident_type'])
            
            # Нормалізація опису
            df['description'] = df['description'].str.strip()
            
            # Перевірка кількості жертв (не може бути від'ємною)
            df['casualties'] = df['casualties'].clip(lower=0)
            df['wounded'] = df['wounded'].clip(lower=0)
            
        elif data_type == 'personnel':
            # Обробка даних про особовий склад
            # Перевірка на дублікати
            df = df.drop_duplicates(subset=['last_name', 'first_name', 'patronymic', 'unit', 'incident_id'])
            
            # Нормалізація імен (перша літера велика, решта малі)
            df['last_name'] = df['last_name'].str.title()
            df['first_name'] = df['first_name'].str.title()
            df['patronymic'] = df['patronymic'].str.title()
            
            # Перевірка статусу
            valid_statuses = ['active', 'wounded', 'killed', 'missing']
            df = df[df['status'].isin(valid_statuses)]
        
        return df.to_dict('records')
    
    def save_operational_data(self, data):
        """
        Збереження оперативних даних у базу даних
        """
        if not data:
            logger.info("Немає нових оперативних даних для збереження")
            return 0
        
        try:
            count = 0
            for item in data:
                self.cursor.execute(
                    """INSERT INTO operational_situation 
                       (timestamp, location, description, threat_level) 
                       VALUES (%s, %s, %s, %s)""", 
                    (item['timestamp'], item['location'], item['description'], item['threat_level'])
                )
                count += 1
            
            self.conn.commit()
            logger.info(f"Збережено {count} нових оперативних записів")
            return count
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Помилка при збереженні оперативних даних: {e}")
            return 0
    
    def save_incident_data(self, data):
        """
        Збереження даних про інциденти у базу даних
        """
        if not data:
            logger.info("Немає нових даних про інциденти для збереження")
            return []
        
        try:
            incident_ids = []
            for item in data:
                self.cursor.execute(
                    """INSERT INTO incidents 
                       (timestamp, location, incident_type, description, casualties, wounded) 
                       VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""", 
                    (item['timestamp'], item['location'], item['incident_type'], 
                     item['description'], item['casualties'], item['wounded'])
                )
                incident_id = self.cursor.fetchone()[0]
                incident_ids.append((incident_id, item['casualties'], item['wounded']))
            
            self.conn.commit()
            logger.info(f"Збережено {len(data)} нових інцидентів")
            return incident_ids
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Помилка при збереженні даних про інциденти: {e}")
            return []
    
    def save_personnel_data(self, data):
        """
        Збереження даних про особовий склад у базу даних
        """
        if not data:
            logger.info("Немає нових даних про особовий склад для збереження")
            return 0
        
        try:
            count = 0
            for item in data:
                self.cursor.execute(
                    """INSERT INTO personnel 
                       (rank, last_name, first_name, patronymic, unit, status, incident_id, injury_description) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
                    (item['rank'], item['last_name'], item['first_name'], item['patronymic'], 
                     item['unit'], item['status'], item['incident_id'], item['injury_description'])
                )
                count += 1
            
            self.conn.commit()
            logger.info(f"Збережено {count} нових записів про особовий склад")
            return count
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Помилка при збереженні даних про особовий склад: {e}")
            return 0
    
    def run_collection_cycle(self):
        """
        Запуск повного циклу збору та обробки даних
        """
        logger.info("Запуск циклу збору та обробки даних...")
        
        if not self.connect_to_db():
            return False
        
        try:
            # Збір та обробка оперативних даних
            operational_data = self.collect_operational_data()
            processed_operational_data = self.preprocess_data(operational_data, 'operational')
            self.save_operational_data(processed_operational_data)
            
            # Збір та обробка даних про інциденти
            incident_data = self.collect_incident_data()
            processed_incident_data = self.preprocess_data(incident_data, 'incident')
            incident_ids = self.save_incident_data(processed_incident_data)
            
            # Збір та обробка даних про особовий склад для кожного інциденту
            for incident_id, casualties, wounded in incident_ids:
                personnel_data = self.collect_personnel_data(incident_id, casualties, wounded)
                processed_personnel_data = self.preprocess_data(personnel_data, 'personnel')
                self.save_personnel_data(processed_personnel_data)
            
            logger.info("Цикл збору та обробки даних успішно завершено")
            return True
        except Exception as e:
            logger.error(f"Помилка при виконанні циклу збору та обробки даних: {e}")
            return False
        finally:
            self.disconnect_from_db()

# Функція для запуску збору даних
def run_data_collection():
    collector = DataCollector()
    return collector.run_collection_cycle()

# Головна функція
def main():
    logger.info("Запуск модуля збору та обробки даних...")
    success = run_data_collection()
    if success:
        logger.info("Модуль збору та обробки даних успішно завершив роботу")
    else:
        logger.error("Модуль збору та обробки даних завершив роботу з помилками")

if __name__ == "__main__":
    main()