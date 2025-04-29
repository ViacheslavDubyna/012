# Головний файл запуску інформаційно-аналітичної системи Національної гвардії України

import os
import argparse
import sys
from flask import Flask
from api import app as api_app
from dashboard import dashboard
from dashboard import improved_dashboard
from dashboard.improved_dashboard_routes import register_dashapp
from database.models import Base
from sqlalchemy import create_engine
from config.config import DB_URL, SERVER_CONFIG

def create_app(disable_ml=False):
    """Створення та налаштування Flask-додатку"""
    app = Flask(__name__)
    
    # Зберігаємо налаштування ML в конфігурації додатку
    app.config['DISABLE_ML'] = disable_ml
    
    # Реєстрація Blueprint для дашборду
    app.register_blueprint(dashboard, url_prefix='/dashboard')
    
    # Реєстрація Blueprint для вдосконаленого дашборду
    app.register_blueprint(improved_dashboard, url_prefix='/dashboard/improved')
    
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--disable-ml', action='store_true', help='Вимкнути ML-функціонал')
    args = parser.parse_args()
    
    # Передаємо параметр disable_ml у функцію create_app
    app = create_app(disable_ml=args.disable_ml)
    
    # Інтеграція Dash-додатку з Flask
    try:
        dispatcher = register_dashapp(app)
    except Exception as e:
        print(f"Помилка при інтеграції Dash з Flask: {e}")
        print("Запуск системи без інтеграції з Dash...")
        dispatcher = app
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'init_db':
            init_db()
            sys.exit(0)
        elif sys.argv[1] == 'seed_db':
            seed_db()
            sys.exit(0)
    
    # Використовуємо dispatcher замість app.run для інтеграції Dash з Flask
    from werkzeug.serving import run_simple
    run_simple(SERVER_CONFIG['host'], SERVER_CONFIG['port'], dispatcher, use_reloader=SERVER_CONFIG['debug'], use_debugger=SERVER_CONFIG['debug'])
    print(f"Інформаційно-аналітична система Національної гвардії України запущена на http://{SERVER_CONFIG['host']}:{SERVER_CONFIG['port']}")

if __name__ == '__main__':
    main()