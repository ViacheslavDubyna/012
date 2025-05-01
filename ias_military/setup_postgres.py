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
            # Використовуємо точне ім'я служби PostgreSQL
            service_name = 'postgresql-x64-17' # Явно вказуємо ім'я служби
            print(f"Перевірка статусу служби: {service_name}")
            cmd = ['sc', 'query', service_name]
            print(f"Виконання команди: {' '.join(cmd)}")
            try:
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='cp866') # Використовуємо text=True та кодування
                stdout, stderr = process.communicate()
                print(f"Вивід stdout:\n{stdout}")
                if stderr:
                    print(f"Вивід stderr:\n{stderr}")
                
                # Перевіряємо стан служби
                if process.returncode == 0 and stdout:
                    # Шукаємо рядок зі станом
                    state_line = next((line for line in stdout.splitlines() if 'STATE' in line), None)
                    if state_line and 'RUNNING' in state_line:
                        print(f"Служба {service_name} знайдена у стані RUNNING.")
                        return True
                    else:
                        print(f"Служба {service_name} не знайдена у стані RUNNING. Поточний стан: {state_line}")
                        return False
                else:
                    print(f"Помилка виконання команди 'sc query' або порожній вивід. Код повернення: {process.returncode}")
                    return False
            except FileNotFoundError:
                print(f"Помилка: Команда 'sc' не знайдена. Переконайтеся, що ви запускаєте скрипт у Windows з відповідними правами.")
                return False
            except Exception as query_err:
                print(f"Неочікувана помилка під час виконання 'sc query': {query_err}")
                return False
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
        if platform.system() == 'Windows': # <-- Додано перевірку платформи
            # Детальне логування пошуку служби
            print('\n[DEBUG] Пошук служб PostgreSQL у виводі SC:')
            cmd_find = ['sc', 'query', 'type=', 'service', 'state=', 'all']
            process = subprocess.Popen(cmd_find, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, _ = process.communicate()
            print(f'[DEBUG] Raw SC output:\n{stdout.decode("utf-8", errors="replace")}')
            
            service_name = None
            lines = stdout.split(b'\r\n')
            for i, line in enumerate(lines):
                # Шукаємо рядок з DISPLAY_NAME, що містить 'postgresql'
                # Важливо: Перевіряємо саме DISPLAY_NAME, бо SERVICE_NAME може бути різним (напр. postgresql-x64-14)
                if b'DISPLAY_NAME' in line and b'postgresql' in line.lower():
                    # Шукаємо SERVICE_NAME у попередніх рядках (зазвичай 1-2 рядки вище)
                    for j in range(max(0, i - 2), i):
                        prev_line = lines[j]
                        if b'SERVICE_NAME:' in prev_line:
                            try:
                                service_name = prev_line.split(b':')[1].strip().decode('utf-8')
                                print(f"[DEBUG] Знайдено службу PostgreSQL: {service_name} (Display: {line.split(b':')[1].strip().decode('utf-8', errors='replace')})")
                                break # Знайшли службу, виходимо з внутрішнього циклу
                            except (IndexError, UnicodeDecodeError) as e:
                                print(f"[DEBUG] Помилка парсингу SERVICE_NAME: {e} для рядка: {prev_line}")
                                continue
                    if service_name: # Якщо знайшли ім'я, виходимо з основного циклу
                        break

            if not service_name:
                print("✗ Служба PostgreSQL не знайдена. Переконайтесь, що:")
                print("  1) PostgreSQL встановлено.")
                print("  2) Служба PostgreSQL запущена або може бути запущена.")
                print("  3) Ім'я служби містить 'postgresql' (перевірте через 'services.msc').")
                print("\n[DEBUG] Повний вивід 'sc query':")
                print(stdout.decode('utf-8', errors='replace'))
                return False
            
            # Запускаємо знайдену службу
            cmd = ['sc', 'start', service_name]
            print(f"\n[DEBUG] Виконуємо команду: {' '.join(cmd)}")
            try:
                # Використовуємо check_output для кращої обробки помилок
                output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, errors='replace')
                print(f"✓ Служба PostgreSQL '{service_name}' успішно запущена.")
                print(f"[DEBUG] Вивід команди запуску:\n{output}")
                time.sleep(3) # Даємо час службі стабілізуватися
                return True
            except subprocess.CalledProcessError as e:
                # Перевіряємо, чи служба вже запущена (код помилки 1056)
                if e.returncode == 1056 or 'already been started' in e.output.lower():
                    print(f"✓ Служба PostgreSQL '{service_name}' вже працює.")
                    time.sleep(1) # Невелика пауза
                    return True
                elif e.returncode == 5: # Access Denied
                    print(f"✗ Помилка доступу під час спроби запуску служби '{service_name}'.")
                    print("  Схоже, скрипту не вистачає прав адміністратора для запуску служби PostgreSQL.")
                    print("  Будь ласка, спробуйте один із варіантів:")
                    print("    1) Перезапустіть цей скрипт (або 'start_system.py') від імені адміністратора.")
                    print("       (Клацніть правою кнопкою миші на файлі -> Запустити від імені адміністратора)")
                    print("    2) Запустіть службу PostgreSQL вручну через 'services.msc' перед запуском скрипта.")
                    print(f"[DEBUG] Помилка: {e.output}")
                    return False
                else:
                    print(f"✗ Помилка запуску служби '{service_name}'. Код: {e.returncode}")
                    print(f"[DEBUG] Помилка: {e.output}")
                    return False
            except FileNotFoundError:
                print(f"✗ Помилка: Команда 'sc' не знайдена. Переконайтеся, що ви запускаєте скрипт з правами адміністратора або 'sc' є в PATH.")
                return False
            except Exception as e:
                print(f"✗ Неочікувана помилка під час запуску служби '{service_name}': {e}")
                import traceback
                print(f"[DEBUG] Трасування стеку:\n{traceback.format_exc()}")
                return False

        elif platform.system() == 'Linux': # <-- Тепер це правильний elif
            print("Спроба запуску PostgreSQL на Linux...")
            try:
                # Спробуємо запустити через systemctl
                cmd = ['sudo', 'systemctl', 'start', 'postgresql']
                # Використовуємо check=True для перевірки коду повернення
                # capture_output=True для отримання stdout/stderr
                result = subprocess.run(cmd, check=True, capture_output=True, text=True, errors='replace')
                print("✓ PostgreSQL служба успішно запущена через systemctl.")
                print(f"[DEBUG] Вивід systemctl: {result.stdout}")
                time.sleep(3) # Даємо час службі стабілізуватися
                return True
            except FileNotFoundError:
                print("✗ Помилка: Команда 'sudo' або 'systemctl' не знайдена. Переконайтесь, що вони встановлені та доступні.")
                return False
            except subprocess.CalledProcessError as e:
                print(f"✗ Помилка запуску PostgreSQL через systemctl. Код: {e.returncode}")
                print(f"[DEBUG] Помилка systemctl:\n{e.stderr}")
                # Тут можна додати спробу запуску через 'service postgresql start', якщо systemctl недоступний або не працює
                return False
            except Exception as e:
                print(f"✗ Неочікувана помилка під час запуску PostgreSQL на Linux: {e}")
                import traceback
                print(f"[DEBUG] Трасування стеку:\n{traceback.format_exc()}")
                return False

        elif platform.system() == 'Darwin': # macOS
            print("Спроба запуску PostgreSQL на macOS...")
            try:
                # Спробуємо запустити через brew services (поширений метод для macOS)
                cmd = ['brew', 'services', 'start', 'postgresql']
                result = subprocess.run(cmd, check=True, capture_output=True, text=True, errors='replace')
                print("✓ PostgreSQL служба успішно запущена через brew services.")
                print(f"[DEBUG] Вивід brew services: {result.stdout}")
                time.sleep(3) # Даємо час службі стабілізуватися
                return True
            except FileNotFoundError:
                print("✗ Помилка: Команда 'brew' не знайдена. Переконайтесь, що Homebrew встановлено та 'brew' є в PATH.")
                return False
            except subprocess.CalledProcessError as e:
                # Перевіряємо, чи служба вже запущена
                if 'already started' in e.stdout.lower() or 'already started' in e.stderr.lower():
                    print(f"✓ Служба PostgreSQL вже працює (виявлено через brew services).")
                    time.sleep(1)
                    return True
                else:
                    print(f"✗ Помилка запуску PostgreSQL через brew services. Код: {e.returncode}")
                    print(f"[DEBUG] Помилка brew services: stdout: {e.stdout} stderr: {e.stderr}")
                    # Можна додати альтернативні методи запуску для macOS (напр. pg_ctl)
                    return False
            except Exception as e:
                print(f"✗ Неочікувана помилка під час запуску PostgreSQL на macOS: {e}")
                import traceback
                print(f"[DEBUG] Трасування стеку:\n{traceback.format_exc()}")
                return False

        else:
            print(f"✗ Непідтримувана ОС: {platform.system()}")
            return False

    # Цей except ловить помилки, що сталися *до* визначення платформи або *поза* логікою запуску для конкретної платформи
    # (наприклад, помилка в самому subprocess.Popen для 'sc query' на Windows)
    except Exception as e:
        import traceback
        # Визначаємо команду, якщо вона була визначена в блоці try
        cmd_str = ' '.join(cmd) if 'cmd' in locals() else 'не визначена на цьому етапі'
        print(f"КРИТИЧНА ПОМИЛКА на етапі ініціалізації запуску PostgreSQL: {e}")
        print(f"Трасування стеку:\n{traceback.format_exc()}")
        return False

def setup_postgres():
    """Налаштування PostgreSQL"""
    # Перевіряємо, чи запущено PostgreSQL
    if not check_postgres_running():
        print("\n✗ Служба PostgreSQL не запущена.")
        print("Будь ласка, запустіть службу PostgreSQL вручну перед продовженням:")
        print("  1. Натисніть Win + R, введіть 'services.msc' та натисніть Enter.")
        print("  2. Знайдіть службу, що містить 'PostgreSQL' (наприклад, 'postgresql-x64-17').")
        print("  3. Клацніть правою кнопкою миші та виберіть 'Запустити'.")
        print("Після запуску служби, будь ласка, перезапустіть систему за допомогою 'start_system.py'.")
        return False # Повертаємо False, якщо служба не запущена
    else:
        print("\n✓ PostgreSQL вже запущено.")

    # Якщо перевірка пройшла успішно, повертаємо True
    return True

if __name__ == '__main__':
    if setup_postgres():
        print("\n=== Налаштування PostgreSQL завершено успішно ===")
    else:
        print("\n=== Налаштування PostgreSQL не вдалося ===")
        # Додамо sys.exit(1) для позначення помилки при прямому запуску
        sys.exit(1)