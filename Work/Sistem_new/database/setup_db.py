#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Скрипт для створення та налаштування бази даних PostgreSQL.
Створює необхідні таблиці та заповнює їх тестовими даними.
"""

import os
import sys
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime, timedelta
import random

# Параметри підключення до бази даних
DB_PARAMS = {
    'dbname': 'ngu_decision_support',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'client_encoding': 'UTF8'
}

# SQL-запити для створення таблиць
CREATE_TABLES = [
    """
    CREATE TABLE IF NOT EXISTS operational_situation (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP NOT NULL,
        location VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
        threat_level INTEGER NOT NULL CHECK (threat_level BETWEEN 1 AND 5),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS incidents (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP NOT NULL,
        location VARCHAR(255) NOT NULL,
        incident_type VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        casualties INTEGER DEFAULT 0,
        wounded INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS personnel (
        id SERIAL PRIMARY KEY,
        rank VARCHAR(50) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        first_name VARCHAR(100) NOT NULL,
        patronymic VARCHAR(100),
        unit VARCHAR(100) NOT NULL,
        status VARCHAR(50) NOT NULL CHECK (status IN ('active', 'wounded', 'killed', 'missing')),
        incident_id INTEGER REFERENCES incidents(id),
        injury_description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS decisions (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP NOT NULL,
        decision_maker VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
        action_taken TEXT NOT NULL,
        result TEXT,
        effectiveness INTEGER CHECK (effectiveness BETWEEN 1 AND 10),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
]

# Функція для створення бази даних
def create_database():
    try:
        # Підключення до PostgreSQL сервера
        conn = psycopg2.connect(
            dbname='postgres',
            user=DB_PARAMS['user'],
            password=DB_PARAMS['password'],
            host=DB_PARAMS['host'],
            port=DB_PARAMS['port'],
            client_encoding='utf8'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Перевірка існування бази даних
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_PARAMS['dbname'],))
        exists = cursor.fetchone()
        
        if not exists:
            # Створення бази даних
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(DB_PARAMS['dbname'])))
            print(f"База даних {DB_PARAMS['dbname']} успішно створена.")
        else:
            print(f"База даних {DB_PARAMS['dbname']} вже існує.")
            
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Помилка при створенні бази даних: {e}")
        return False

# Функція для створення таблиць
def create_tables():
    try:
        # Підключення до створеної бази даних
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        
        # Створення таблиць
        for create_table_query in CREATE_TABLES:
            cursor.execute(create_table_query)
        
        conn.commit()
        print("Таблиці успішно створені.")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Помилка при створенні таблиць: {e}")
        return False

# Функція для генерації тестових даних
def generate_test_data():
    try:
        # Підключення до бази даних
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        
        # Очищення таблиць перед заповненням
        cursor.execute("TRUNCATE TABLE personnel CASCADE")
        cursor.execute("TRUNCATE TABLE incidents CASCADE")
        cursor.execute("TRUNCATE TABLE operational_situation CASCADE")
        cursor.execute("TRUNCATE TABLE decisions CASCADE")
        conn.commit()
        
        # Генерація даних для operational_situation
        locations = ['Харків', 'Донецьк', 'Луганськ', 'Запоріжжя', 'Херсон', 'Миколаїв', 'Суми', 'Чернігів']
        descriptions = [
            'Активні бойові дії', 'Артилерійські обстріли', 'Ракетні удари', 
            'Повітряна тривога', 'Диверсійна діяльність', 'Відносно спокійно'
        ]
        
        now = datetime.now()
        for i in range(20):
            timestamp = now - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
            location = random.choice(locations)
            description = random.choice(descriptions)
            threat_level = random.randint(1, 5)
            
            cursor.execute(
                """INSERT INTO operational_situation 
                   (timestamp, location, description, threat_level) 
                   VALUES (%s, %s, %s, %s)""", 
                (timestamp, location, description, threat_level)
            )
        
        # Генерація даних для incidents
        incident_types = ['Артобстріл', 'Ракетний удар', 'Атака БПЛА', 'Мінометний обстріл', 'Снайперський вогонь']
        incident_descriptions = [
            'Масований обстріл позицій', 'Точковий удар по об\'єкту', 
            'Обстріл житлових районів', 'Атака на блокпост', 'Обстріл транспортного засобу'
        ]
        
        for i in range(15):
            timestamp = now - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
            location = random.choice(locations)
            incident_type = random.choice(incident_types)
            description = random.choice(incident_descriptions)
            casualties = random.randint(0, 5)
            wounded = random.randint(0, 10)
            
            cursor.execute(
                """INSERT INTO incidents 
                   (timestamp, location, incident_type, description, casualties, wounded) 
                   VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""", 
                (timestamp, location, incident_type, description, casualties, wounded)
            )
            incident_id = cursor.fetchone()[0]
        
            # Генерація даних для personnel, пов'язаних з інцидентом
            if casualties > 0 or wounded > 0:
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
                                      'Множинні травми', 'Опіки', 'Ампутація кінцівки']
                
                for j in range(casualties + wounded):
                    rank = random.choice(ranks)
                    last_name = random.choice(last_names)
                    first_name = random.choice(first_names)
                    patronymic = random.choice(patronymics)
                    unit = random.choice(units)
                    
                    if j < casualties:
                        status = 'killed'
                        injury_description = None
                    else:
                        status = 'wounded'
                        injury_description = random.choice(injury_descriptions)
                    
                    cursor.execute(
                        """INSERT INTO personnel 
                           (rank, last_name, first_name, patronymic, unit, status, incident_id, injury_description) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
                        (rank, last_name, first_name, patronymic, unit, status, incident_id, injury_description)
                    )
        
        # Генерація даних для decisions
        decision_makers = ['Командувач НГУ', 'Начальник штабу', 'Командир бригади', 'Командир батальйону']
        decision_descriptions = [
            'Рішення про передислокацію підрозділів', 'Рішення про посилення оборони', 
            'Рішення про евакуацію особового складу', 'Рішення про контратаку', 
            'Рішення про зміну тактики ведення бою'
        ]
        actions_taken = [
            'Передислокація підрозділів', 'Посилення оборонних позицій', 
            'Евакуація особового складу', 'Проведення контратаки', 
            'Зміна тактики ведення бою', 'Запит додаткових ресурсів'
        ]
        results = [
            'Успішне виконання', 'Часткове виконання', 'Виконання з втратами', 
            'Невиконання через зміну обстановки', 'Відкладено через погіршення ситуації'
        ]
        
        for i in range(10):
            timestamp = now - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
            decision_maker = random.choice(decision_makers)
            description = random.choice(decision_descriptions)
            action_taken = random.choice(actions_taken)
            result = random.choice(results)
            effectiveness = random.randint(1, 10)
            
            cursor.execute(
                """INSERT INTO decisions 
                   (timestamp, decision_maker, description, action_taken, result, effectiveness) 
                   VALUES (%s, %s, %s, %s, %s, %s)""", 
                (timestamp, decision_maker, description, action_taken, result, effectiveness)
            )
        
        conn.commit()
        print("Тестові дані успішно згенеровані.")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Помилка при генерації тестових даних: {e}")
        return False

# Головна функція
def main():
    print("Налаштування бази даних для системи підтримки прийняття рішень ГУ НГУ...")
    
    if create_database():
        if create_tables():
            generate_test_data()
    
    print("Налаштування бази даних завершено.")

if __name__ == "__main__":
    main()