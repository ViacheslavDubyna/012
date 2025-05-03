#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Конфігураційний файл для інформаційно-аналітичної системи ДПСУ
"""

import os
from dotenv import load_dotenv

# Завантажуємо змінні середовища з .env файлу, якщо він існує
load_dotenv()

class Config:
    """Базовий клас конфігурації"""
    # Загальні налаштування
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dpsu-ias-secret-key-change-in-production')
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'
    TESTING = False
    
    # Налаштування бази даних
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'dpsu_ias')
    
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Шляхи до директорій
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODELS_DIR = os.path.join(BASE_DIR, 'models')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    
    # Налаштування API
    API_VERSION = '1.0'
    API_TITLE = 'ДПСУ ІАС API'
    API_DESCRIPTION = 'API для інформаційно-аналітичної системи Державної прикордонної служби України'
    
    # Налаштування логування
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.path.join(BASE_DIR, 'logs', 'dpsu_ias.log')

class DevelopmentConfig(Config):
    """Конфігурація для розробки"""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    """Конфігурація для тестування"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """Конфігурація для продакшену"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') # Обов'язково має бути встановлено в продакшені
    
    # Додаткові налаштування безпеки для продакшену
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

# Вибір конфігурації в залежності від середовища
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Поточна конфігурація
Config = config_by_name[os.environ.get('FLASK_ENV', 'default')]