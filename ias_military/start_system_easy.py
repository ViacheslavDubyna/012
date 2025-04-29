# Скрипт для спрощеного запуску інформаційно-аналітичної системи Національної гвардії України
# Автоматично перевіряє наявність PostgreSQL, налаштовує базу даних та запускає веб-інтерфейс

import os
import sys
import time
import subprocess
import platform
import webbrowser
import winreg
import ctypes
import shutil
from pathlib import Path

# Додаємо шлях до батьківської директорії в sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Імпортуємо необхідні модулі
from setup_postgres import setup_postgres, check_postgres_running
from config.config import SERVER_CONFIG

def print_header(message):
    """Виведення заголовка з форматуванням"""
    print("\n" + "=" * 80)
    print(f" {message} ".center(80, "="))
    print("=" * 80)

def check_postgres_installed():
    """Перевірка, чи встановлено PostgreSQL"""
    print_header("Перевірка наявності PostgreSQL")
    
    try:
        if platform.system() == 'Windows':
            # Перевіряємо наявність PostgreSQL в реєстрі Windows
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\PostgreSQL") as key:
                    print("PostgreSQL встановлено (знайдено в реєстрі).")
                    return True
            except WindowsError:
                # Перевіряємо наявність служби PostgreSQL
                cmd = ['sc', 'query', 'postgresql']
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if process.returncode == 0:
                    print("PostgreSQL встановлено (знайдено службу).")
                    return True
                
                # Перевіряємо наявність виконуваного файлу psql
                paths = os.environ["PATH"].split(os.pathsep)
                for path in paths:
                    psql_path = os.path.join(path, "psql.exe")
                    if os.path.exists(psql_path):
                        print("PostgreSQL встановлено (знайдено psql.exe).")
                        return True
                
                print("PostgreSQL не встановлено або не знайдено.")
                return False
        else:
            # Для Linux/Mac перевіряємо наявність команди psql
            cmd = ['which', 'psql']
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode == 0:
                print("PostgreSQL встановлено.")
                return True
            else:
                print("PostgreSQL не встановлено або не знайдено.")
                return False
    except Exception as e:
        print(f"Помилка при перевірці наявності PostgreSQL: {e}")
        return False

def download_postgres():
    """Завантаження PostgreSQL"""
    print_header("Завантаження PostgreSQL")
    
    if platform.system() == 'Windows':
        print("Відкриваємо сторінку завантаження PostgreSQL...")
        webbrowser.open("https://www.postgresql.org/download/windows/")
        print("\nБудь ласка, виконайте наступні кроки:")
        print("1. Завантажте та встановіть PostgreSQL з офіційного сайту")
        print("2. Під час встановлення запам'ятайте пароль для користувача 'postgres'")
        print("3. Після завершення встановлення поверніться до цього вікна та натисніть Enter")
        
        input("\nНатисніть Enter після завершення встановлення PostgreSQL...")
        return check_postgres_installed()
    else:
        print("Для автоматичного встановлення PostgreSQL на Linux/Mac використовуйте відповідний пакетний менеджер:")
        if platform.system() == 'Darwin':  # macOS
            print("brew install postgresql")
        else:  # Linux
            print("sudo apt update && sudo apt install postgresql postgresql-contrib")
        
        input("\nНатисніть Enter після завершення встановлення PostgreSQL...")
        return check_postgres_installed()

def init_database():
    """Ініціалізація бази даних"""
    print_header("Ініціалізація бази даних")
    try:
        # Імпортуємо функцію з run.py
        from run import init_db
        init_db()
        print("База даних успішно ініціалізована.")
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
        print("База даних успішно заповнена тестовими даними.")
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

def create_desktop_shortcut():
    """Створення ярлика на робочому столі"""
    print_header("Створення ярлика на робочому столі")
    
    try:
        if platform.system() == 'Windows':
            # Отримуємо шлях до робочого столу
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            
            # Шлях до поточного скрипта
            script_path = os.path.abspath(__file__)
            
            # Шлях до Python інтерпретатора
            python_path = sys.executable
            
            # Створюємо .bat файл для запуску скрипта
            shortcut_path = os.path.join(desktop, "ІАС НГУ.bat")
            
            with open(shortcut_path, 'w', encoding='utf-8') as f:
                f.write(f'@echo off\n')
                f.write(f'echo Запуск інформаційно-аналітичної системи Національної гвардії України...\n')
                f.write(f'"{python_path}" "{script_path}" --no-shortcut\n')
                f.write(f'pause\n')
            
            print(f"Ярлик створено на робочому столі: {shortcut_path}")
            return True
        else:
            # Для Linux створюємо .desktop файл
            if platform.system() == 'Linux':
                home = os.path.expanduser("~")
                desktop = os.path.join(home, "Desktop")
                
                if not os.path.exists(desktop):
                    desktop = os.path.join(home, "Робочий стіл")  # Для українських локалізацій
                
                script_path = os.path.abspath(__file__)
                python_path = sys.executable
                
                shortcut_path = os.path.join(desktop, "ІАС НГУ.desktop")
                
                with open(shortcut_path, 'w', encoding='utf-8') as f:
                    f.write("[Desktop Entry]\n")
                    f.write("Type=Application\n")
                    f.write("Name=ІАС НГУ\n")
                    f.write(f"Exec={python_path} {script_path} --no-shortcut\n")
                    f.write("Terminal=true\n")
                    f.write("Comment=Інформаційно-аналітична система Національної гвардії України\n")
                
                # Встановлюємо права на виконання
                os.chmod(shortcut_path, 0o755)
                
                print(f"Ярлик створено на робочому столі: {shortcut_path}")
                return True
            # Для macOS створюємо AppleScript
            elif platform.system() == 'Darwin':
                home = os.path.expanduser("~")
                desktop = os.path.join(home, "Desktop")
                
                script_path = os.path.abspath(__file__)
                python_path = sys.executable
                
                shortcut_path = os.path.join(desktop, "ІАС НГУ.command")
                
                with open(shortcut_path, 'w', encoding='utf-8') as f:
                    f.write("#!/bin/bash\n")
                    f.write(f"cd {os.path.dirname(script_path)}\n")
                    f.write(f"{python_path} {script_path} --no-shortcut\n")
                
                # Встановлюємо права на виконання
                os.chmod(shortcut_path, 0o755)
                
                print(f"Ярлик створено на робочому столі: {shortcut_path}")
                return True
    except Exception as e:
        print(f"Помилка при створенні ярлика: {e}")
    
    return False

def start_system():
    """Запуск всієї системи"""
    print_header("Запуск інформаційно-аналітичної системи Національної гвардії України")
    
    # Перевіряємо аргументи командного рядка
    no_shortcut = "--no-shortcut" in sys.argv
    
    # Створюємо ярлик, якщо потрібно
    if not no_shortcut:
        create_desktop_shortcut()
    
    # Перевіряємо наявність PostgreSQL
    if not check_postgres_installed():
        print("PostgreSQL не встановлено. Спроба завантаження...")
        if not download_postgres():
            print("Не вдалося встановити PostgreSQL. Система не може працювати без бази даних.")
            input("Натисніть Enter для завершення...")
            return False
    
    # Перевіряємо, чи запущено PostgreSQL
    if not check_postgres_running():
        print("PostgreSQL не запущено. Спроба запуску...")
        from setup_postgres import start_postgres
        if not start_postgres():
            print("Не вдалося запустити PostgreSQL. Перевірте, чи встановлено PostgreSQL.")
            input("Натисніть Enter для завершення...")
            return False
        # Даємо час на запуск PostgreSQL
        time.sleep(5)
    
    # Налаштування бази даних
    print("Налаштування бази даних...")
    if not setup_postgres():
        print("Помилка при налаштуванні бази даних.")
        input("Натисніть Enter для завершення...")
        return False
    
    # Ініціалізація бази даних
    if not init_database():
        print("Помилка при ініціалізації бази даних.")
        input("Натисніть Enter для завершення...")
        return False
    
    # Заповнення бази даних тестовими даними
    if not seed_database():
        print("Помилка при заповненні бази даних тестовими даними.")
        input("Натисніть Enter для завершення...")
        return False
    
    # Запуск веб-інтерфейсу
    if not start_web_interface():
        print("Помилка при запуску веб-інтерфейсу. Перевірте налаштування та спробуйте знову.")
        input("Натисніть Enter для завершення...")
        return False
    
    return True

if __name__ == '__main__':
    start_system()