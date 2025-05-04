# Скрипт для запуску інформаційно-аналітичної системи Національної гвардії України

import os
import sys
import time
import subprocess
import platform
import webbrowser
import subprocess
import ctypes
import logging # Додано імпорт logging
from setup_postgres import setup_postgres, check_postgres_running
from config.config import SERVER_CONFIG
from flask import Flask

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[
    logging.StreamHandler(sys.stdout) # Виводити логи в stdout
])

def print_header(message):
    """Виведення заголовка з форматуванням"""
    log_msg = "\n" + "=" * 80 + "\n" + f" {message} ".center(80, "=") + "\n" + "=" * 80
    logging.info(log_msg) # Змінено print на logging

def init_database():
    """Ініціалізація бази даних"""
    logging.info("Початок ініціалізації бази даних...") # Додано логування
    print_header("Ініціалізація бази даних")
    try:
        # Імпортуємо функцію з run.py
        from run import init_db
        init_db() # Виклик функції, яка вже має логування
        logging.info("Ініціалізація бази даних завершена успішно.") # Додано логування
        return True
    except Exception as e:
        logging.error(f"Помилка при ініціалізації бази даних: {e}", exc_info=True) # Змінено print на logging
        return False

def seed_database():
    """Заповнення бази даних тестовими даними"""
    logging.info("Початок заповнення бази даних тестовими даними...") # Додано логування
    print_header("Заповнення бази даних тестовими даними")
    try:
        # Імпортуємо функцію з run.py
        from run import seed_db
        seed_db() # Виклик функції, яка вже має логування
        logging.info("Заповнення бази даних тестовими даними завершено успішно.") # Додано логування
        return True
    except Exception as e:
        logging.error(f"Помилка при заповненні бази даних: {e}", exc_info=True) # Змінено print на logging
        return False

def start_web_interface():
    """Запуск веб-інтерфейсу системи"""
    logging.info("Початок запуску веб-інтерфейсу...") # Додано логування
    print_header("Запуск веб-інтерфейсу системи")
    try:
        # Імпортуємо функцію з run.py
        from run import main as run_main # Імпортуємо main з run.py
        logging.info("Виклик main() з run.py для запуску сервера...")
        run_main() # Запускаємо головну функцію з run.py
        logging.info("Веб-інтерфейс успішно запущено (run_main завершив роботу, хоча не мав би).") # Малоймовірно, що дійде сюди
        return True
    except ImportError as e:
        logging.error(f"Помилка імпорту: Не вдалося імпортувати необхідні компоненти з run.py: {e}", exc_info=True)
        return False
    except Exception as e:
        logging.error(f"Помилка при запуску веб-інтерфейсу: {e}", exc_info=True) # Змінено print на logging
        return False

def check_admin_rights():
    """Перевірка наявності прав адміністратора"""
    logging.info("Перевірка прав адміністратора...") # Додано логування
    try:
        is_admin = (os.getuid() == 0) if platform.system() != "Windows" else ctypes.windll.shell32.IsUserAnAdmin()
        logging.info(f"Права адміністратора: {'Є' if is_admin else 'Немає'}") # Додано логування
        return is_admin
    except AttributeError:
        # У випадку, якщо getuid() недоступний (не Unix-подібна система без ctypes)
        logging.warning("Не вдалося визначити права адміністратора.")
        return False
    except Exception as e:
        logging.error(f"Помилка при перевірці прав адміністратора: {e}", exc_info=True)
        return False

def run_as_admin():
    """Перезапуск скрипта з правами адміністратора"""
    logging.warning("Спроба перезапуску скрипта з правами адміністратора...")
    if platform.system() == "Windows":
        try:
            logging.info("Використання ctypes для перезапуску з правами адміністратора у Windows.")
            result = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            logging.info(f"Результат ShellExecuteW: {result}")
            if result <= 32:
                logging.error(f"Не вдалося перезапустити скрипт з правами адміністратора. Код помилки: {result}")
                return False
            else:
                logging.info("Скрипт успішно запитав підвищення прав.")
                return True # Успішно запитано підвищення
        except Exception as e:
            logging.error(f"Помилка при спробі перезапуску з правами адміністратора: {e}", exc_info=True)
            return False
    else:
        # Для Linux/macOS (потребує sudo)
        logging.warning("Для запуску з правами адміністратора на Linux/macOS, будь ласка, використовуйте 'sudo python start_system.py'")
        return False

def main():
    """Головна функція запуску системи"""
    logging.info("Початок виконання main() у start_system.py")

    # Перевірка та запит прав адміністратора (якщо потрібно для PostgreSQL)
    # if not check_admin_rights():
    #     print("Для налаштування та запуску PostgreSQL можуть знадобитися права адміністратора.")
    #     if run_as_admin():
    #         sys.exit(0) # Вихід, оскільки скрипт перезапускається
    #     else:
    #         print("Не вдалося отримати права адміністратора. Продовження без них може призвести до помилок.")
    # else:
    #     print("Скрипт запущено з правами адміністратора.")

    # 1. Налаштування PostgreSQL
    print_header("Налаштування PostgreSQL")
    logging.info("Початок налаштування PostgreSQL...")
    if setup_postgres():
        logging.info("Налаштування PostgreSQL завершено успішно.")
        # Перевірка, чи запущено PostgreSQL
        if not check_postgres_running():
            logging.error("PostgreSQL не запущено після налаштування. Подальший запуск системи неможливий.")
            sys.exit(1)
        else:
            logging.info("PostgreSQL успішно запущено.")
    else:
        logging.error("Помилка під час налаштування PostgreSQL. Запуск системи скасовано.")
        sys.exit(1)

    # 2. Ініціалізація бази даних
    if not init_database():
        logging.error("Не вдалося ініціалізувати базу даних. Запуск системи скасовано.")
        sys.exit(1)

    # 3. Заповнення бази даних тестовими даними (опціонально)
    # Можна додати перевірку, чи потрібно заповнювати БД
    if not seed_database():
        logging.warning("Не вдалося заповнити базу даних тестовими даними. Продовження роботи...")
        # Не критична помилка, можна продовжити

    # 4. Запуск веб-інтерфейсу
    if not start_web_interface():
        logging.critical("Не вдалося запустити веб-інтерфейс. Система не може працювати.")
        sys.exit(1)
    else:
        # Цей блок коду, ймовірно, ніколи не виконається, оскільки start_web_interface() запускає блокуючий сервер
        logging.info("Веб-інтерфейс запущено (теоретично). Скрипт start_system.py завершує роботу.")

if __name__ == "__main__":
    logging.info(f"Запуск скрипта start_system.py як головного (__name__ == '__main__')")
    main()
    logging.info("Скрипт start_system.py завершив свою роботу.") # Цей лог може не з'явитися, якщо сервер блокує

def check_dependencies():
    """Перевірка наявності всіх необхідних залежностей"""
    print_header("Перевірка наявності необхідних залежностей")
    
    # Визначаємо шлях до папки зі скриптом
    script_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_path = os.path.join(script_dir, 'requirements.txt')

    # Читаємо requirements.txt, щоб отримати список пакетів
    required_packages = []
    try:
        with open(requirements_path, 'r') as f:
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
        print(f"Помилка: Файл {requirements_path} не знайдено.")
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
        print(f"\nВиявлено відсутні пакети. Спроба встановлення з {requirements_path}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
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
                  print(f"✗ Не вдалося встановити/знайти всі необхідні залежності. Перевірте файл {requirements_path} та вивід pip.")
                  return False
        except subprocess.CalledProcessError as e:
            print(f"✗ Помилка під час виконання 'pip install -r {requirements_path}': {e}")
            print(f"  Перевірте файл {requirements_path} та наявність pip.")
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
            # Визначаємо шлях до папки зі скриптом для повідомлення про помилку
            script_dir = os.path.dirname(os.path.abspath(__file__))
            requirements_path = os.path.join(script_dir, 'requirements.txt')
            print("Виявлено проблеми з залежностями. Спробуйте встановити їх вручну:")
            # Додаємо лапки навколо шляху на випадок пробілів
            print(f'pip install -r "{requirements_path}"')
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
    
    # 5. Запуск веб-інтерфейсу через run.py
    print_header("Запуск веб-інтерфейсу системи")
    try:
        # Визначаємо шлях до інтерпретатора Python
        python_executable = sys.executable
        run_script_path = os.path.join(os.path.dirname(__file__), 'run.py')
        
        # Перевіряємо наявність --disable-ml аргументу
        run_args = [python_executable, run_script_path]
        if '--disable-ml' in sys.argv:
            run_args.append('--disable-ml')
            
        print(f"Запуск команди: {' '.join(run_args)}")
        
        # Запускаємо run.py як окремий процес
        # Ми не чекаємо завершення процесу, оскільки це веб-сервер
        process = subprocess.Popen(run_args, cwd=os.path.dirname(__file__))
        
        # Виводимо інформацію про запуск (URL беремо з конфігурації)
        host = SERVER_CONFIG['host']
        port = SERVER_CONFIG['port']
        url = f"http://{'127.0.0.1' if host == '0.0.0.0' else host}:{port}"
        print(f"\nВеб-інтерфейс повинен бути доступний за адресою: {url}")
        print(f"Дашборд: {url}/dashboard/improved")
        print("Сервер запущено у фоновому режимі. Натисніть Ctrl+C для зупинки, якщо потрібно.")
        
        # Відкриваємо браузер
        def open_browser_thread():
            time.sleep(5) # Даємо більше часу на запуск сервера
            print(f"Спроба відкрити {url} у браузері...")
            try:
                webbrowser.open(url)
                print("Браузер відкрито.")
            except Exception as browser_err:
                print(f"Не вдалося автоматично відкрити браузер: {browser_err}")
                print(f"Будь ласка, відкрийте {url} вручну.")

        import threading
        browser_thread = threading.Thread(target=open_browser_thread)
        browser_thread.start()
        
        # Очікуємо завершення процесу сервера (необов'язково, але може бути корисним для логування)
        # process.wait() # Розкоментуйте, якщо хочете, щоб start_system чекав завершення run.py

    except Exception as e:
        import traceback
        print(f"\n✗ Помилка запуску run.py: {e}")
        print(f"Трасування стеку:\n{traceback.format_exc()}")
        sys.exit(1)
    
    return True

if __name__ == '__main__':
    # Перевірка прав адміністратора видалена