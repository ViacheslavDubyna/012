# Головний файл запуску інформаційно-аналітичної системи Національної гвардії України

import os
import argparse
import sys
import logging # Додано імпорт logging
from flask import Flask
from api import app as api_app
# Видалено імпорт старого дашборду та improved_dashboard Blueprint
# from dashboard import dashboard
# from dashboard import improved_dashboard
# Видалено імпорт init_dash
# from dashboard.improved_dashboard_routes import init_dash
from database.models import Base
from sqlalchemy import create_engine
from config.config import DB_URL, SERVER_CONFIG
# Імпортуємо DispatcherMiddleware
from werkzeug.middleware.dispatcher import DispatcherMiddleware
# Імпортуємо сам Dash додаток
from dashboard.improved_dashboard_integration import app as dash_app

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_app(disable_ml=False):
    """Створення та налаштування Flask-додатку"""
    app = Flask(__name__)
    
    # Зберігаємо налаштування ML в конфігурації додатку
    app.config['DISABLE_ML'] = disable_ml
    
    # Реєстрація Blueprint для дашборду (старий, якщо потрібен)
    # app.register_blueprint(dashboard, url_prefix='/dashboard')
    
    # Реєстрація Blueprint для вдосконаленого дашборду (більше не потрібна тут)
    # app.register_blueprint(improved_dashboard, url_prefix='/dashboard/improved')
    
    # Реєстрація API маршрутів
    app.register_blueprint(api_app, url_prefix='/api')
    
    logging.info("Flask app створено.") # Додано логування
    return app

def init_db():
    from sqlalchemy import create_engine, text
    import os
    DB_URL = os.environ.get('DB_URL', 'postgresql://postgres:postgres@localhost:5432/ngu_ias')
    engine = create_engine(DB_URL)
    # Перевіряємо, чи є таблиці в базі
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"))
        table_count = result.scalar()
        if table_count == 0:
            # Якщо таблиць немає, виконуємо init_db.sql
            sql_path = os.path.join(os.path.dirname(__file__), 'database', 'init_db.sql')
            with open(sql_path, 'r', encoding='utf-8') as f:
                sql = f.read()
            for statement in sql.split(';'):
                stmt = statement.strip()
                if stmt:
                    conn.execute(text(stmt))
            print('Базу даних ініціалізовано через init_db.sql')
    # Далі стандартна ініціалізація моделей
    from database.models import Base
    Base.metadata.create_all(engine)
    from database.seed import seed_database
    seed_database(DB_URL)
    logging.info("База даних успішно ініціалізована.") # Змінено print на logging

def seed_db():
    """Заповнення бази даних тестовими даними"""
    from database.seed import seed_database
    seed_database(DB_URL)
    logging.info("База даних успішно заповнена тестовими даними.") # Змінено print на logging

def register_dashapp(flask_app):
    """Інтеграція Dash-додатку з Flask через DispatcherMiddleware"""
    from werkzeug.middleware.dispatcher import DispatcherMiddleware
    from dashboard.improved_dashboard_integration import app as dash_app
    dispatcher = DispatcherMiddleware(flask_app, { '/dashboard/improved': dash_app.server })
    logging.info("Dash app зареєстровано через DispatcherMiddleware.") # Додано логування
    return dispatcher

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--disable-ml', action='store_true', help='Вимкнути ML-функціонал')
    args = parser.parse_args()
    
    logging.info(f"Запуск main() з параметрами: disable_ml={args.disable_ml}") # Додано логування
    
    # Передаємо параметр disable_ml у функцію create_app
    app = create_app(disable_ml=args.disable_ml)
    
    # Інтеграція Dash-додатку з Flask за допомогою DispatcherMiddleware
    logging.info("Налаштування DispatcherMiddleware для Dash...") # Змінено print на logging
    # Створюємо middleware, монтуючи сервер Dash під потрібним префіксом
    # Важливо: dash_app.server - це Flask сервер, який лежить в основі Dash додатку
    # Префікс '/dashboard/improved' відповідає routes_pathname_prefix у Dash
    dispatcher = DispatcherMiddleware(app, {
        '/dashboard/improved': dash_app.server
    })
    logging.info("DispatcherMiddleware налаштовано.") # Змінено print на logging
    
    # Видалено старий код інтеграції через init_dash
    # print("Початок інтеграції Dash...")
    # try:
    #     init_dash(app)
    #     print("Інтеграція Dash успішна.")
    # except Exception as e:
    #     print(f"Помилка при інтеграції Dash з Flask: {e}")
    #     print("Продовження запуску Flask без інтеграції Dash...")
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'init_db':
            init_db()
            sys.exit(0)
        elif sys.argv[1] == 'seed_db':
            seed_db()
            sys.exit(0)
    
    # Запускаємо Flask додаток через DispatcherMiddleware
    logging.info("Спроба запуску сервера через DispatcherMiddleware...") # Змінено print на logging
    from werkzeug.serving import run_simple
    # Використовуємо dispatcher замість app
    # Вимикаємо use_reloader, щоб уникнути проблем з ініціалізацією під час перезапуску
    host = SERVER_CONFIG['host']
    port = SERVER_CONFIG['port']
    debug = SERVER_CONFIG['debug']
    logging.info(f"Намагаюся запустити сервер на {host}:{port} з debug={debug}...") # Змінено print на logging
    try:
        logging.info("Перед викликом run_simple з dispatcher...") # Змінено print на logging
        run_simple(host, port, dispatcher, use_reloader=False, use_debugger=debug)
        # Цей рядок, ймовірно, не буде виконано, оскільки run_simple блокує
        logging.info(f"Інформаційно-аналітична система Національної гвардії України запущена на http://{host}:{port}") # Змінено print на logging
    except OSError as e:
        logging.error(f"Помилка OSError під час запуску run_simple (можливо, порт зайнятий?): {e}") # Змінено print на logging
        raise
    except Exception as e:
        logging.error(f"Загальна помилка під час запуску run_simple: {e}") # Змінено print на logging
        raise # Перевикидаємо помилку для кращої діагностики

if __name__ == '__main__':
    main()