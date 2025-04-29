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
    print("\n=== Перевірка статусу PostgreSQL ===")
    try:
        # Команда для перевірки статусу PostgreSQL
        if platform.system() == 'Windows':
            # Шукаємо точну назву служби PostgreSQL
            cmd_find = ['sc', 'query', 'type=', 'service', 'state=', 'all']
            process = subprocess.Popen(cmd_find, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, _ = process.communicate()
            
            # Шукаємо службу з ім'ям, що містить 'PostgreSQL'
            postgres_services = [line.split(b'postgresql')[0].strip() for line in stdout.split(b'\r\n') if b'postgresql' in line.lower()]
            if not postgres_services:
                return False
                
            service_name = postgres_services[0].decode('utf-8')
            cmd = ['sc', 'query', service_name]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, _ = process.communicate()
            return b'RUNNING' in stdout
        else:
            # Для Linux/Mac використовуємо systemctl або pg_isready
            cmd = ['pg_isready']
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            print(f"Статус PostgreSQL: {'запущено' if process.returncode == 0 else 'не запущено'}")
            return process.returncode == 0
    except Exception as e:
        import traceback
        print(f"ПОМИЛКА ПЕРЕВІРКИ СТАТУСУ: {e}\nТрасування стеку:\n{traceback.format_exc()}")
        return False

def start_postgres():
    """Запуск PostgreSQL"""
    print("\n=== Спроба запуску PostgreSQL ===")
    try:
        # Детальне логування пошуку служби
        print('\n[DEBUG] Пошук служб PostgreSQL у виводі SC:')
        cmd_find = ['sc', 'query', 'type=', 'service', 'state=', 'all']
        process = subprocess.Popen(cmd_find, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = process.communicate()
        print(f'[DEBUG] Raw SC output:\n{stdout.decode("utf-8", errors="replace")}')
        
        postgres_services = []  # Список для зберігання імен служб PostgreSQL
        for line in stdout.split(b'\r\n'):
            if b'POSTGRESQL' in line.upper() or b'postgresql' in line.lower():
                # Шукаємо ім'я служби в рядку
                parts = line.split()
                if parts and parts[0]:
                    postgres_services.append(parts[0])
        if not postgres_services:
            print("Служба PostgreSQL не знайдена. Переконайтесь, що:")
            print("1) PostgreSQL встановлено\n2) Служба має 'PostgreSQL' в назві")
            print("Доступні служби:")
            print(stdout.decode('utf-8', errors='replace'))
            return False
            
        service_name = postgres_services[0].decode('utf-8') if isinstance(postgres_services[0], bytes) else postgres_services[0]
        
        # Запускаємо знайдену службу
        # Перевіряємо, чи містить ім'я служби префікс 'SERVICE_NAME:'
        if 'SERVICE_NAME:' in service_name:
            # Видаляємо префікс 'SERVICE_NAME:' та пробіли
            service_name = service_name.replace('SERVICE_NAME:', '').strip()
        
        cmd = ['sc', 'start', service_name]
        print(f'\n[DEBUG] Виконуємо команду: {" ".join(cmd)}')
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"PostgreSQL служба {service_name} успішно запущена.")
            print(f"[DEBUG] Стан служби:\n{result.stdout}")
            return True
        else:
            print(f"Помилка запуску служби. Код: {result.returncode}")
            print(f"[DEBUG] Помилка:\n{result.stderr}")
            return False
    except Exception as e:
        import traceback
        print(f"КРИТИЧНА ПОМИЛКА: Не вдалося запустити PostgreSQL\nДеталі: {e}\nКоманда: {' '.join(cmd)}")
        print(f"Трасування стеку:\n{traceback.format_exc()}")
        return False
    else:
        # Для Linux/Mac використовуємо systemctl
        cmd = ['sudo', 'systemctl', 'start', 'postgresql']
        subprocess.run(cmd, check=True)
        print("PostgreSQL успішно запущено.")
        return True

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
        import traceback
        print(f"ПОМИЛКА НАЛАШТУВАННЯ БАЗИ: {e}\nТрасування стеку:\n{traceback.format_exc()}")
        return False

if __name__ == '__main__':
    setup_postgres()