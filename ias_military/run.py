# Головний файл запуску інформаційно-аналітичної системи Національної гвардії України

import os
import sys
from flask import Flask
from api import app as api_app
from dashboard import dashboard
from database.models import Base
from sqlalchemy import create_engine
from config.config import DB_URL, SERVER_CONFIG

def create_app():
    """Створення та налаштування Flask-додатку"""
    app = Flask(__name__)
    
    # Реєстрація Blueprint для дашборду
    app.register_blueprint(dashboard, url_prefix='/dashboard')
    
    # Реєстрація API маршрутів
    app.register_blueprint(api_app, url_prefix='/api')
    
    return app

def init_db():
    """Ініціалізація бази даних"""
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
    print("База даних успішно ініціалізована.")

def seed_db():
    """Заповнення бази даних тестовими даними"""
    from database.seed import seed_database
    seed_database(DB_URL)
    print("База даних успішно заповнена тестовими даними.")

if __name__ == '__main__':
    # Створюємо додаток
    app = create_app()
    
    # Перевіряємо аргументи командного рядка
    if len(sys.argv) > 1:
        if sys.argv[1] == 'init_db':
            init_db()
            sys.exit(0)
        elif sys.argv[1] == 'seed_db':
            seed_db()
            sys.exit(0)
    
    # Запускаємо додаток
    app.run(
        debug=SERVER_CONFIG['debug'], 
        host=SERVER_CONFIG['host'], 
        port=SERVER_CONFIG['port']
    )
    print(f"Інформаційно-аналітична система Національної гвардії України запущена на http://{SERVER_CONFIG['host']}:{SERVER_CONFIG['port']}")