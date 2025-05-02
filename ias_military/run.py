# Головний файл запуску інформаційно-аналітичної системи Національної гвардії України

import os
import argparse
import sys
from flask import Flask
from api import app as api_app
from dashboard import dashboard
from dashboard import improved_dashboard
from dashboard.improved_dashboard_routes import init_dash
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
    
    # Інтеграція Dash-додатку з Flask за допомогою init_app
    print("Початок інтеграції Dash...")
    try:
        init_dash(app)
        print("Інтеграція Dash успішна.")
    except Exception as e:
        print(f"Помилка при інтеграції Dash з Flask: {e}")
        print("Продовження запуску Flask без інтеграції Dash...")
    
    # dispatcher більше не потрібен, оскільки init_dash налаштовує маршрутизацію в app
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'init_db':
            init_db()
            sys.exit(0)
        elif sys.argv[1] == 'seed_db':
            seed_db()
            sys.exit(0)
    
    # Запускаємо Flask додаток (Dash інтегровано через init_dash)
    print("Спроба запуску Flask сервера...")
    from werkzeug.serving import run_simple
    # Використовуємо app замість dispatcher
    # Вимикаємо use_reloader, щоб уникнути проблем з ініціалізацією під час перезапуску
    host = SERVER_CONFIG['host']
    port = SERVER_CONFIG['port']
    debug = SERVER_CONFIG['debug']
    print(f"Намагаюся запустити сервер на {host}:{port} з debug={debug}...")
    try:
        print("Перед викликом run_simple...")
        run_simple(host, port, app, use_reloader=False, use_debugger=debug)
        # Цей рядок, ймовірно, не буде виконано, оскільки run_simple блокує
        print(f"Інформаційно-аналітична система Національної гвардії України запущена на http://{host}:{port}")
    except OSError as e:
        print(f"Помилка OSError під час запуску run_simple (можливо, порт зайнятий?): {e}")
        raise
    except Exception as e:
        print(f"Загальна помилка під час запуску run_simple: {e}")
        raise # Перевикидаємо помилку для кращої діагностики

if __name__ == '__main__':
    main()