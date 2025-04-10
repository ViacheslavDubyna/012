# Скрипт для налаштування бази даних PostgreSQL

import os
import sys
import subprocess
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Додаємо шлях до батьківської директорії в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Імпортуємо конфігурацію
from config.config import DB_CONFIG

def setup_database():
    """Налаштування бази даних PostgreSQL"""
    try:
        # Підключення до PostgreSQL сервера
        conn = psycopg2.connect(
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port']
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Перевірка, чи існує база даних
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_CONFIG['database'],))
        exists = cursor.fetchone()
        
        if not exists:
            # Створення бази даних
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(DB_CONFIG['database'])
            ))
            print(f"База даних {DB_CONFIG['database']} успішно створена.")
        else:
            print(f"База даних {DB_CONFIG['database']} вже існує.")
        
        # Закриття з'єднання з сервером PostgreSQL
        cursor.close()
        conn.close()
        
        # Виконання SQL-скрипта для ініціалізації бази даних
        sql_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'init_db.sql')
        
        # Формування команди для виконання SQL-скрипта
        cmd = [
            'psql',
            '-U', DB_CONFIG['user'],
            '-h', DB_CONFIG['host'],
            '-p', DB_CONFIG['port'],
            '-d', DB_CONFIG['database'],
            '-f', sql_script_path
        ]
        
        # Встановлення змінної середовища для пароля PostgreSQL
        env = os.environ.copy()
        env['PGPASSWORD'] = DB_CONFIG['password']
        
        # Виконання команди
        process = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            print("SQL-скрипт успішно виконано.")
        else:
            print(f"Помилка при виконанні SQL-скрипта: {stderr.decode()}")
        
        return True
    
    except Exception as e:
        print(f"Помилка при налаштуванні бази даних: {e}")
        return False

if __name__ == '__main__':
    setup_database()