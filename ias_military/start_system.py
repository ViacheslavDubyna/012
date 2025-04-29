# Скрипт для запуску інформаційно-аналітичної системи Національної гвардії України

import os
import sys
import time
import subprocess
import platform
import webbrowser
from setup_postgres import setup_postgres, check_postgres_running
from config.config import SERVER_CONFIG

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
        
        # Запускаємо додаток
        app.run(
            debug=SERVER_CONFIG['debug'], 
            host=SERVER_CONFIG['host'], 
            port=SERVER_CONFIG['port']
        )
        return True
    except Exception as e:
        print(f"Помилка при запуску веб-інтерфейсу: {e}")
        return False

def start_system():
    """Запуск всієї системи"""
    print_header("Запуск інформаційно-аналітичної системи Національної гвардії України")
    
    # Перевіряємо аргументи командного рядка
    skip_db_setup = False
    skip_db_init = False
    skip_db_seed = False
    
    if len(sys.argv) > 1:
        if "--help" in sys.argv or "-h" in sys.argv:
            print("Використання: python start_system.py [опції]")
            print("Опції:")
            print("  --skip-db-setup    Пропустити налаштування PostgreSQL")
            print("  --skip-db-init     Пропустити ініціалізацію бази даних")
            print("  --skip-db-seed     Пропустити заповнення бази даних тестовими даними")
            print("  --help, -h         Показати цю довідку")
            sys.exit(0)
        
        skip_db_setup = "--skip-db-setup" in sys.argv
        skip_db_init = "--skip-db-init" in sys.argv
        skip_db_seed = "--skip-db-seed" in sys.argv
    
    # Налаштування PostgreSQL
    if not skip_db_setup:
        if not setup_postgres():
            print("Помилка при налаштуванні PostgreSQL. Перевірте налаштування та спробуйте знову.")
            return False
    else:
        print("Пропускаємо налаштування PostgreSQL...")
        # Перевіряємо, чи запущено PostgreSQL
        if not check_postgres_running():
            print("PostgreSQL не запущено. Запустіть PostgreSQL перед продовженням.")
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