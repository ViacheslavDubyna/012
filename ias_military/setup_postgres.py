# Скрипт для налаштування PostgreSQL для інформаційно-аналітичної системи НГУ

import os
import sys
import subprocess
import platform
import time

# Додаємо шлях до батьківської директорії в sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Імпортуємо конфігурацію
from config.config import DB_CONFIG

def check_postgres_running():
    """Перевірка, чи запущено PostgreSQL"""
    try:
        # Команда для перевірки статусу PostgreSQL
        if platform.system() == 'Windows':
            # Для Windows використовуємо SC
            cmd = ['sc', 'query', 'postgresql']
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            return b'RUNNING' in stdout
        else:
            # Для Linux/Mac використовуємо systemctl або pg_isready
            cmd = ['pg_isready']
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.communicate()
            return process.returncode == 0
    except Exception as e:
        print(f"Помилка при перевірці статусу PostgreSQL: {e}")
        return False

def start_postgres():
    """Запуск PostgreSQL"""
    try:
        if platform.system() == 'Windows':
            # Для Windows використовуємо SC
            cmd = ['sc', 'start', 'postgresql']
            subprocess.run(cmd, check=True)
            print("PostgreSQL успішно запущено.")
            return True
        else:
            # Для Linux/Mac використовуємо systemctl
            cmd = ['sudo', 'systemctl', 'start', 'postgresql']
            subprocess.run(cmd, check=True)
            print("PostgreSQL успішно запущено.")
            return True
    except Exception as e:
        print(f"Помилка при запуску PostgreSQL: {e}")
        print("Спробуйте запустити PostgreSQL вручну.")
        return False

def setup_postgres():
    """Налаштування PostgreSQL"""
    # Перевіряємо, чи запущено PostgreSQL
    if not check_postgres_running():
        print("PostgreSQL не запущено. Спроба запуску...")
        if not start_postgres():
            print("Не вдалося запустити PostgreSQL. Перевірте, чи встановлено PostgreSQL.")
            return False
        # Даємо час на запуск PostgreSQL
        time.sleep(5)
    
    # Налаштування бази даних
    from database.setup_db import setup_database
    if setup_database():
        print("База даних успішно налаштована.")
        return True
    else:
        print("Помилка при налаштуванні бази даних.")
        return False

if __name__ == '__main__':
    setup_postgres()