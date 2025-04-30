# Скрипт для запуску інформаційно-аналітичної системи Національної гвардії України

import os
import sys
import time
import subprocess
import platform
import webbrowser
from setup_postgres import setup_postgres, check_postgres_running
from config.config import SERVER_CONFIG
from flask import Flask

def print_header(message):
    """Виведення заголовка з форматуванням"""
    print("\n" + "=" * 80)
    print(f" {message} ".center(80, "="))
    print("=" * 80)

def init_database():
    """Ініціалізація бази даних"""
    print_header("Ініціалізація бази даних")
    try:
        # Імпортуємо функцію з run.py
        from run import init_db
        init_db()
        return True
    except Exception as e:
        print(f"Помилка при ініціалізації бази даних: {e}")
        return False

def seed_database():
    """Заповнення бази даних тестовими даними"""
    print_header("Заповнення бази даних тестовими даними")
    try:
        # Імпортуємо функцію з run.py
        from run import seed_db
        seed_db()
        return True
    except Exception as e:
        print(f"Помилка при заповненні бази даних: {e}")
        return False

def start_web_interface():
    """Запуск веб-інтерфейсу системи"""
    print_header("Запуск веб-інтерфейсу системи")
    try:
        # Імпортуємо функцію з run.py
        from run import create_app
        app = create_app()
        with app.app_context():
            pass
        
        # Виводимо інформацію про запуск
        host = SERVER_CONFIG['host']
        port = SERVER_CONFIG['port']
        url = f"http://{'localhost' if host == '0.0.0.0' else host}:{port}"
        
        print(f"Інформаційно-аналітична система запускається за адресою: {url}")
        print(f"Дашборд буде доступний за адресою: {url}/dashboard")
        print(f"API буде доступне за адресою: {url}/api")
        
        # Відкриваємо браузер з невеликою затримкою
        def open_browser():
            time.sleep(2)  # Даємо час на запуск сервера
            webbrowser.open(url)
        
        # Запускаємо браузер у окремому потоці
        import threading
        threading.Thread(target=open_browser).start()
        
        # Запускаємо додаток через dispatcher для інтеграції Dash
        from run import register_dashapp
        from werkzeug.serving import run_simple
        try:
            dispatcher = register_dashapp(app)
        except Exception as e:
            print(f"Помилка при інтеграції Dash з Flask: {e}")
            print("Запуск системи без інтеграції з Dash...")
            dispatcher = app
            
        run_simple(host, port, dispatcher, use_reloader=SERVER_CONFIG['debug'], use_debugger=SERVER_CONFIG['debug'])
        return True
    except Exception as e:
        print(f"Помилка при запуску веб-інтерфейсу: {e}")
        return False

def check_dependencies():
    """Перевірка наявності всіх необхідних залежностей"""
    print_header("Перевірка наявності необхідних залежностей")
    
    # Читаємо requirements.txt, щоб отримати список пакетів
    required_packages = []
    try:
        with open('requirements.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Видаляємо специфікацію версії (==, >=, <=, > , <)
                    package_name = line.split('==')[0].split('>=')[0].split('<=')[0].split('>')[0].split('<')[0]
                    # Зіставлення імен пакетів з requirements.txt з іменами для імпорту
                    import_name_map = {
                        'scikit-learn': 'sklearn',
                        'python-dateutil': 'dateutil',
                        'psycopg2-binary': 'psycopg2',
                        'Werkzeug': 'werkzeug', # Ім'я модуля з маленької літери
                        'Jinja2': 'jinja2',     # Ім'я модуля з маленької літери
                        'MarkupSafe': 'markupsafe' # Ім'я модуля з маленької літери
                        # Пакети dash-* є частиною dash, їх не треба перевіряти окремо
                    }
                    # Виключаємо компоненти dash з перевірки
                    dash_components = ['dash-core-components', 'dash-html-components', 'dash-table']
                    if package_name not in dash_components:
                        import_name = import_name_map.get(package_name, package_name)
                        required_packages.append(import_name)
    except FileNotFoundError:
        print("Помилка: Файл requirements.txt не знайдено.")
        return False
    
    print(f"Перевірка пакетів: {', '.join(required_packages)}")
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} встановлено")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} не встановлено")
    
    if missing_packages:
        print("\nВиявлено відсутні пакети. Спроба встановлення з requirements.txt...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✓ Усі залежності успішно встановлено з requirements.txt")
            # Повторна перевірка після встановлення
            print("Повторна перевірка залежностей...")
            all_installed = True
            # Перевіряємо тільки ті пакети, які ми додали до required_packages (з правильними іменами для імпорту)
            for import_name in required_packages:
                 try:
                     __import__(import_name)
                     print(f"✓ {import_name} тепер встановлено")
                 except ImportError:
                     # Спробуємо знайти оригінальне ім'я пакету для повідомлення про помилку
                     original_name = import_name # За замовчуванням
                     for req_name, imp_name in import_name_map.items():
                         if imp_name == import_name:
                             original_name = req_name
                             break
                     print(f"✗ Пакет '{original_name}' (імпорт як '{import_name}') все ще не встановлено після спроби встановлення.")
                     all_installed = False
            if not all_installed:
                  print("✗ Не вдалося встановити/знайти всі необхідні залежності. Перевірте файл requirements.txt та вивід pip.")
                  return False
        except subprocess.CalledProcessError as e:
            print(f"✗ Помилка під час виконання 'pip install -r requirements.txt': {e}")
            print("  Перевірте файл requirements.txt та наявність pip.")
            return False
        except Exception as e:
            print(f"✗ Непередбачена помилка під час встановлення залежностей: {e}")
            return False

    return True

def start_system():
    """Запуск всієї системи"""
    print_header("Запуск інформаційно-аналітичної системи Національної гвардії України")
    
    # Перевіряємо аргументи командного рядка
    skip_db_setup = False
    skip_db_init = False
    skip_db_seed = False
    skip_dependency_check = False
    
    if len(sys.argv) > 1:
        if "--help" in sys.argv or "-h" in sys.argv:
            print("Використання: python start_system.py [опції]")
            print("Опції:")
            print("  --skip-db-setup    Пропустити налаштування PostgreSQL")
            print("  --skip-db-init     Пропустити ініціалізацію бази даних")
            print("  --skip-db-seed     Пропустити заповнення бази даних тестовими даними")
            print("  --skip-dependency-check  Пропустити перевірку залежностей")
            print("  --help, -h         Показати цю довідку")
            sys.exit(0)
        
        skip_db_setup = "--skip-db-setup" in sys.argv
        skip_db_init = "--skip-db-init" in sys.argv
        skip_db_seed = "--skip-db-seed" in sys.argv
        skip_dependency_check = "--skip-dependency-check" in sys.argv
    
    # Перевірка залежностей
    if not skip_dependency_check:
        if not check_dependencies():
            print("Виявлено проблеми з залежностями. Спробуйте встановити їх вручну:")
            print("pip install -r requirements.txt")
            print("Або запустіть систему з параметром --skip-dependency-check")
            sys.exit(1)
    else:
        print("Пропускаємо перевірку залежностей...")
    
    # Налаштування PostgreSQL
    if not skip_db_setup:
        if not setup_postgres():
            print("Помилка при налаштуванні PostgreSQL. Перевірте налаштування та спробуйте знову.")
            print("Переконайтеся, що PostgreSQL встановлено та служба запущена.")
            return False
    else:
        print("Пропускаємо налаштування PostgreSQL...")
        # Перевіряємо, чи запущено PostgreSQL
        if not check_postgres_running():
            print("PostgreSQL не запущено. Спроба запуску...")
            from setup_postgres import start_postgres
            if not start_postgres():
                print("Не вдалося запустити PostgreSQL. Перевірте налаштування та спробуйте знову.")
                print("Можливо, потрібно запустити службу PostgreSQL вручну через 'services.msc'.")
                return False
    
    # Ініціалізація бази даних
    if not skip_db_init:
        if not init_database():
            print("Помилка при ініціалізації бази даних. Перевірте налаштування та спробуйте знову.")
            return False
    else:
        print("Пропускаємо ініціалізацію бази даних...")
    
    # Заповнення бази даних тестовими даними
    if not skip_db_seed:
        if not seed_database():
            print("Помилка при заповненні бази даних. Перевірте налаштування та спробуйте знову.")
            return False
    else:
        print("Пропускаємо заповнення бази даних тестовими даними...")
    
    # Запуск веб-інтерфейсу
    if not start_web_interface():
        print("Помилка при запуску веб-інтерфейсу. Перевірте налаштування та спробуйте знову.")
        return False
    
    return True

if __name__ == '__main__':
    start_system()