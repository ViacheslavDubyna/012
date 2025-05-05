#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль для генерації тестових даних для інформаційно-аналітичної системи НГУ

Цей модуль містить функції для створення синтетичних даних для тестування
та демонстрації функціональності системи.
"""

import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker
from werkzeug.security import generate_password_hash

from database.models import Incident, BorderCrossing, User, Report
from database import db

# Ініціалізація генератора фейкових даних
fake = Faker('uk_UA')

# Місця інфедентів
CHECKPOINTS = [
    'Київ', 'Львів', 'Полтава', 'Харків', 'Сміла',
    'Донецьк', 'Краматорськ', 'Бердянськ', 'Чернігів', 'Житомир',
    'Дніпро', 'Бориспіль', 'Луганськ', 'Вінниця'
]

# Локації для інцидентів
LOCATIONS = [
    'Львівська область', 'Волинська область', 'Закарпатська область',
    'Чернівецька область', 'Одеська область', 'Вінницька область',
    'Івано-Франківська область', 'Рівненська область', 'Житомирська область',
    'Чернігівська область', 'Сумська область', 'Харківська область',
    'Луганська область', 'Донецька область', 'Запорізька область',
    'Херсонська область', 'Миколаївська область'
]

# Координати для локацій (приблизні)
LOCATION_COORDINATES = {
    'Львівська область': '49.839683,24.029717',
    'Волинська область': '50.747233,25.325383',
    'Закарпатська область': '48.621025,22.288229',
    'Чернівецька область': '48.292079,25.935837',
    'Одеська область': '46.482526,30.723309',
    'Вінницька область': '49.233083,28.468217',
    'Івано-Франківська область': '48.922633,24.711117',
    'Рівненська область': '50.619900,26.251617',
    'Житомирська область': '50.254300,28.658600',
    'Чернігівська область': '51.498400,31.289400',
    'Сумська область': '50.907700,34.798100',
    'Харківська область': '49.992467,36.231267',
    'Луганська область': '48.574000,39.307700',
    'Донецька область': '48.015883,37.802850',
    'Запорізька область': '47.838800,35.139567',
    'Херсонська область': '46.635417,32.616867',
    'Миколаївська область': '46.975033,31.994583'
}

# Типи інцидентів
INCIDENT_TYPES = [
    'Порушення громадського порядку',
    'Масові заворушення',
    'Терористичний акт або його загроза',
    'Незаконне зберігання або носіння зброї',
    'Виявлення підозрілих предметів або вибухових пристроїв',
    'Надзвичайна ситуація техногенного або природного характеру',
    'Протидія диверсійно-розвідувальним групам',
    'Збройний напад на військовий обʼєкт',
    'Виявлення безпілотних літальних апаратів',
    'Замінування обʼєктів критичної інфраструктури',
    'Несанкціоноване проникнення на режимний обʼєкт',
    'Спроба викрадення або пошкодження техніки НГУ',
    'Інцидент з військовослужбовцем (дисциплінарний або кримінальний)',
    'Спроба блокування пересування підрозділів НГУ',
    'Порушення умов комендантської години',
]

# Рівні загрози
SEVERITY_LEVELS = ['низька', 'середня', 'висока']

# Статуси інцидентів
STATUS_TYPES = ['активний', 'вирішений', 'архівований']

# Типи транспортних засобів
VEHICLE_TYPES = ['легковий', 'вантажний', 'автобус', 'пішохід']

# Напрямки перетину
DIRECTIONS = ['в\'їзд', 'виїзд']

# Ролі користувачів
USER_ROLES = ['адміністратор', 'аналітик', 'оператор']

# Типи звітів
REPORT_TYPES = ['щоденний', 'тижневий', 'місячний', 'спеціальний']


def generate_incidents(count=100):
    """
Генерація тестових інцидентів 

:param count: кількість інцидентів для генерації
:return: список об'єктів Incident
    """
    incidents = []
    
    for _ in range(count):
        # Вибір випадкової локації та типу інциденту
        location = random.choice(LOCATIONS)
        incident_type = random.choice(INCIDENT_TYPES)
        
        # Створення випадкової дати за останні 6 місяців
        days_ago = random.randint(0, 180)
        incident_date = datetime.now() - timedelta(days=days_ago)
        
        # Створення інциденту
        incident = Incident(
            title=f"{incident_type} біля {location}",
            description=fake.text(max_nb_chars=500),
            location=location,
            coordinates=LOCATION_COORDINATES.get(location, ''),
            severity=random.choice(SEVERITY_LEVELS),
            status=random.choice(STATUS_TYPES),
            created_at=incident_date,
            updated_at=incident_date + timedelta(hours=random.randint(1, 48))
        )
        
        incidents.append(incident)
    
    return incidents


def generate_border_crossings(count=500):
    """
Генерація тестових даних про подію

:param count: кількість записів для генерації
:return: список об'єктів BorderCrossing
    """
    crossings = []
    
    for _ in range(count):
        # Вибір випадкового населеного пункту
        checkpoint = random.choice(CHECKPOINTS)
        direction = random.choice(DIRECTIONS)
        vehicle_type = random.choice(VEHICLE_TYPES)
        
        # Створення випадкової дати за останні 6 місяців
        days_ago = random.randint(0, 180)
        crossing_date = datetime.now().date() - timedelta(days=days_ago)
        
        # Кількість подій (більше для одних, менше для віншихних)
        if vehicle_type == 'надзвичайна подія':
            count_value = random.randint(50, 500)
        elif vehicle_type == 'злочин':
            count_value = random.randint(10, 100)
        elif vehicle_type == 'правопорушення':
            count_value = random.randint(5, 30)
        else:  # злочинець
            count_value = random.randint(20, 200)
        
        # Створення запису про подію
        crossing = BorderCrossing(
            checkpoint=checkpoint,
            direction=direction,
            vehicle_type=vehicle_type,
            count=count_value,
            date=crossing_date,
            created_at=datetime.combine(crossing_date, datetime.min.time())
        )
        
        crossings.append(crossing)
    
    return crossings


def generate_users(count=20):
    """
Генерація тестових користувачів системи

:param count: кількість користувачів для генерації
:return: список об'єктів User
    """
    users = []
    
    # Створення адміністратора за замовчуванням
    admin = User(
        username='admin',
        email='admin@dpsu.gov.ua',
        password_hash=generate_password_hash('admin123'),
        role='адміністратор',
        is_active=True,
        created_at=datetime.now() - timedelta(days=365),
        last_login=datetime.now() - timedelta(hours=random.randint(1, 72))
    )
    users.append(admin)
    
    # Створення інших користувачів
    for i in range(1, count):
        # Генерація унікального імені користувача
        username = f"{fake.last_name().lower()}_{fake.first_name().lower()}"
        
        # Створення користувача
        user = User(
            username=username,
            email=f"{username}@dpsu.gov.ua",
            password_hash=generate_password_hash(f"password{i}"),
            role=random.choice(USER_ROLES),
            is_active=random.random() > 0.1,  # 90% користувачів активні
            created_at=datetime.now() - timedelta(days=random.randint(1, 365)),
            last_login=datetime.now() - timedelta(days=random.randint(0, 30))
        )
        
        users.append(user)
    
    return users


def generate_reports(users, count=50):
    """
Генерація тестових звітів

:param users: список користувачів, які можуть створювати звіти
:param count: кількість звітів для генерації
:return: список об'єктів Report
    """
    reports = []
    
    # Відфільтруємо користувачів, які можуть створювати звіти (адміністратори та аналітики)
    report_creators = [user for user in users if user.role in ['адміністратор', 'аналітик']]
    
    if not report_creators:
        return reports
    
    for _ in range(count):
        # Вибір випадкового типу звіту та користувача
        report_type = random.choice(REPORT_TYPES)
        user = random.choice(report_creators)
        
        # Створення випадкової дати за останні 6 місяців
        days_ago = random.randint(0, 180)
        report_date = datetime.now() - timedelta(days=days_ago)
        
        # Створення заголовка звіту в залежності від типу
        if report_type == 'щоденний':
            title = f"Щоденний звіт за {report_date.strftime('%d.%m.%Y')}"
        elif report_type == 'тижневий':
            week_start = report_date - timedelta(days=report_date.weekday())
            week_end = week_start + timedelta(days=6)
            title = f"Тижневий звіт {week_start.strftime('%d.%m.%Y')} - {week_end.strftime('%d.%m.%Y')}"
        elif report_type == 'місячний':
            title = f"Місячний звіт за {report_date.strftime('%m.%Y')}"
        else:  # спеціальний
            title = f"Спеціальний звіт: {fake.sentence()}"
        
        # Створення звіту
        report = Report(
            title=title,
            content=fake.text(max_nb_chars=2000),
            report_type=report_type,
            created_by=user.id,
            created_at=report_date,
            updated_at=report_date
        )
        
        reports.append(report)
    
    return reports


def generate_training_data_for_incident_predictor(count=1000):
    """
Генерація тренувальних даних для моделі прогнозування інцидентів

:param count: кількість записів для генерації
:return: кортеж (X, y) з ознаками та цільовими значеннями
    """
    # Створення випадкових ознак
    data = {
        'день_тижня': np.random.randint(0, 7, count),  # 0-6 (пн-нд)
        'місяць': np.random.randint(1, 13, count),  # 1-12
        'кількість_подій': np.random.normal(1000, 300, count),
        'температура': np.random.normal(15, 10, count),
        'опади': np.random.normal(2, 5, count),
        'свято': np.random.choice([0, 1], count, p=[0.9, 0.1]),
        'попередні_інциденти_7днів': np.random.poisson(3, count)
    }
    
    # Створення цільової змінної (рівень загрози)
    # Використовуємо деякі залежності для реалістичності
    y = []
    for i in range(count):
        # Більше інцидентів у вихідні, влітку, під час свят і при більшій кількості подій
        risk_score = 0
        
        # Вихідні дні (5-6 це сб-нд)
        if data['день_тижня'][i] >= 5:
            risk_score += 0.2
        
        # Літні місяці (6-8 це червень-серпень)
        if 6 <= data['місяць'][i] <= 8:
            risk_score += 0.15
        
        # Велика кількість подій
        if data['кількість_перетинів'][i] > 1200:
            risk_score += 0.2
        
        # Свята
        if data['свято'][i] == 1:
            risk_score += 0.3
        
        # Попередні інциденти
        if data['попередні_інциденти_7днів'][i] > 5:
            risk_score += 0.25
        
        # Додаємо випадковість
        risk_score += np.random.normal(0, 0.1)
        
        # Визначаємо рівень загрози
        if risk_score < 0.3:
            y.append('низький')
        elif risk_score < 0.6:
            y.append('середній')
        else:
            y.append('високий')
    
    # Перетворюємо дані у DataFrame
    X = pd.DataFrame(data)
    
    return X, np.array(y)


def generate_training_data_for_border_crossing_predictor(count=1000):
    """
Генерація тренувальних даних для моделі прогнозування правопорушень

:param count: кількість записів для генерації
:return: кортеж (X, y) з ознаками та цільовими значеннями
    """
    # Створення випадкових ознак
    data = {
        'день_тижня': np.random.randint(0, 7, count),  # 0-6 (пн-нд)
        'місяць': np.random.randint(1, 13, count),  # 1-12
        'пункт_патруля_id': np.random.randint(0, len(CHECKPOINTS), count),
        'напрямок': np.random.choice([0, 1], count),  # 0 - в'їзд', 1 - виїзд
        'свято': np.random.choice([0, 1], count, p=[0.9, 0.1]),
        'вихідний': np.random.choice([0, 1], count, p=[0.7, 0.3]),
        'середня_кількість_за_7днів': np.random.normal(1000, 200, count)
    }
    
    # Створення цільової змінної (кількість перетинів)
    y = []
    for i in range(count):
        # Базова кількість
        base_count = 800
        
        # Більше порушень у вихідні
        if data['вихідний'][i] == 1:
            base_count += 300
        
        # Більше порушень влітку (6-8 це червень-серпень)
        if 6 <= data['місяць'][i] <= 8:
            base_count += 200
        
        # Більше порушень у свята
        if data['свято'][i] == 1:
            base_count += 400
        
        # Різні пункти пблокпостів мають різну завантаженість
        checkpoint_factor = 0.7 + (data['пункт_пропуску_id'][i] / len(CHECKPOINTS)) * 0.6
        base_count *= checkpoint_factor
        
        # Додаємо тренд на основі середньої кількості за 7 днів
        trend_factor = data['середня_кількість_за_7днів'][i] / 1000
        base_count *= trend_factor
        
        # Додаємо випадковість
        base_count *= np.random.normal(1, 0.15)
        
        y.append(max(0, int(base_count)))
    
    # Перетворюємо дані у DataFrame
    X = pd.DataFrame(data)
    
    return X, np.array(y)


def generate_training_data_for_resource_predictor(count=1000):
    """
Генерація тренувальних даних для моделі прогнозування необхідних ресурсів

:param count: кількість записів для генерації
:return: кортеж (X, y) з ознаками та цільовими значеннями
    """
    # Створення випадкових ознак
    data = {
        'день_тижня': np.random.randint(0, 7, count),  # 0-6 (пн-нд)
        'місяць': np.random.randint(1, 13, count),  # 1-12
        'прогноз_порушень': np.random.normal(1000, 300, count),
        'рівень_загрози': np.random.choice(['низький', 'середній', 'високий'], count, p=[0.7, 0.2, 0.1]),
        'довжина_лінії охорони_км': np.random.normal(50, 10, count),
        'кількість_блокпостів': np.random.randint(1, 5, count)
    }
    
    # Перетворення категоріальних ознак
    threat_level_map = {'низький': 1, 'середній': 2, 'високий': 3}
    data['рівень_загрози_числовий'] = [threat_level_map[level] for level in data['рівень_загрози']]
    
    # Створення цільової змінної (кількість персоналу)
    y = []
    for i in range(count):
        # Базова кількість персоналу
        base_personnel = 20
        
        # Додаємо персонал в залежності від кількості порушень
        base_personnel += data['прогноз_перетинів'][i] / 50
        
        # Додаємо персонал в залежності від рівня загрози
        base_personnel *= 0.8 + (data['рівень_загрози_числовий'][i] * 0.2)
        
        # Додаємо персонал в залежності від довжини лінії охорони
        base_personnel += data['довжина_кордону_км'][i] / 5
        
        # Додаємо персонал в залежності від кількості блокпостів
        base_personnel += data['кількість_пунктів_пропуску'][i] * 5
        
        # Додаємо випадковість
        base_personnel *= np.random.normal(1, 0.1)
        
        y.append(max(10, int(base_personnel)))
    
    # Видаляємо проміжну ознаку
    del data['рівень_загрози_числовий']
    
    # Перетворюємо дані у DataFrame
    X = pd.DataFrame(data)
    
    return X, np.array(y)


def populate_database():
    """
Заповнення бази даних тестовими даними
    """
    # Генерація користувачів
    users = generate_users(20)
    for user in users:
        db.session.add(user)
    db.session.commit()
    
    # Генерація інцидентів
    incidents = generate_incidents(100)
    for incident in incidents:
        db.session.add(incident)
    db.session.commit()
    
    # Генерація даних про подію
    crossings = generate_border_crossings(500)
    for crossing in crossings:
        db.session.add(crossing)
    db.session.commit()
    
    # Генерація звітів
    reports = generate_reports(users, 50)
    for report in reports:
        db.session.add(report)
    db.session.commit()
    
    print("База даних успішно заповнена тестовими даними.")


if __name__ == "__main__":
    # Цей код виконується тільки при прямому запуску скрипта
    from ias_NGU.run import app
    with app.app_context():
        populate_database()