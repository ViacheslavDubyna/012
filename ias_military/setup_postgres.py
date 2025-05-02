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
            # Динамічний пошук служби PostgreSQL
            service_name = find_postgres_service_name()
            if not service_name:
                print("Не вдалося автоматично визначити ім'я служби PostgreSQL.")
                print("Перевірте, чи встановлено PostgreSQL та чи містить ім'я служби 'postgresql'.")
                return False

            print(f"Перевірка статусу служби: {service_name}")
            cmd = ['sc', 'query', service_name]
            print(f"Виконання команди: {' '.join(cmd)}")
            try:
                # Використовуємо відповідне кодування для Windows (часто cp1251 або cp866)
                # Спробуємо визначити системне кодування
                import locale
                encoding = locale.getpreferredencoding()
                print(f"Використовується кодування: {encoding}")

                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding=encoding, errors='replace')
                stdout, stderr = process.communicate()
                print(f"Вивід stdout:\n{stdout}")
                if stderr:
                    print(f"Вивід stderr:\n{stderr}")

                # Перевіряємо стан служби
                if process.returncode == 0 and stdout:
                    # Шукаємо рядок зі станом
                    state_line = next((line for line in stdout.splitlines() if 'STATE' in line.upper()), None)
                    if state_line and 'RUNNING' in state_line.upper():
                        print(f"Служба {service_name} знайдена у стані RUNNING.")
                        return True
                    else:
                        print(f"Служба {service_name} не знайдена у стані RUNNING. Поточний стан: {state_line}")
                        return False
                else:
                    # Код 1060 означає, що служба не існує
                    if process.returncode == 1060 or (stderr and '1060' in stderr):
                         print(f"Служба {service_name} не знайдена (код 1060). Можливо, PostgreSQL не встановлено або ім'я служби інше.")
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
            # Для Linux/Mac використовуємо pg_isready (більш надійний)
            try:
                cmd = ['pg_isready', '-q', '-h', DB_CONFIG.get('host', 'localhost'), '-p', str(DB_CONFIG.get('port', '5432')), '-U', DB_CONFIG.get('user', 'postgres')]
                print(f"Виконання команди: {' '.join(cmd)}")
                # Не передаємо пароль через командний рядок з міркувань безпеки
                # pg_isready зазвичай не потребує пароля для перевірки статусу
                process = subprocess.run(cmd, timeout=5, check=True, capture_output=True, text=True)
                print(f"pg_isready виконано успішно. Статус: запущено.")
                return True
            except FileNotFoundError:
                print("Команда 'pg_isready' не знайдена. Переконайтесь, що клієнтські утиліти PostgreSQL встановлені та доступні в PATH.")
                return False
            except subprocess.TimeoutExpired:
                print("Перевірка статусу PostgreSQL через pg_isready зайняла занадто багато часу.")
                return False
            except subprocess.CalledProcessError as pg_err:
                print(f"pg_isready повернув помилку (код {pg_err.returncode}). Статус: не запущено або проблема з підключенням.")
                print(f"Stderr: {pg_err.stderr}")
                return False
            except Exception as e:
                print(f"Неочікувана помилка під час виконання pg_isready: {e}")
                return False
    except Exception as e:
        import traceback
        print(f"ПОМИЛКА ПЕРЕВІРКИ СТАТУСУ: {e}\nТрасування стеку:\n{traceback.format_exc()}")
        return False

def find_postgres_service_name():
    """Знаходить ім'я служби PostgreSQL у Windows."""
    if platform.system() != 'Windows':
        return None

    print("\n[DEBUG] Пошук імені служби PostgreSQL...")
    try:
        import locale
        encoding = locale.getpreferredencoding()
        cmd_find = ['sc', 'query', 'type=', 'service', 'state=', 'all', 'bufsize=', '8000'] # Збільшено буфер
        process = subprocess.Popen(cmd_find, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding=encoding, errors='replace')
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"[DEBUG] Помилка виконання 'sc query': {stderr}")
            return None

        # print(f'[DEBUG] Raw SC output для пошуку служби:\n{stdout}') # Розкоментувати для детального логування

        service_name = None
        lines = stdout.splitlines()
        for i, line in enumerate(lines):
            # Шукаємо рядок з DISPLAY_NAME, що містить 'postgresql'
            if 'DISPLAY_NAME' in line.upper() and 'postgresql' in line.lower():
                # Шукаємо SERVICE_NAME у попередніх рядках
                for j in range(max(0, i - 2), i):
                    prev_line = lines[j]
                    if 'SERVICE_NAME:' in prev_line.upper():
                        try:
                            found_name = prev_line.split(':', 1)[1].strip()
                            # Додаткова перевірка, щоб уникнути служб типу pgAgent
                            if 'postgresql' in found_name.lower() and 'agent' not in found_name.lower():
                                service_name = found_name
                                print(f"[DEBUG] Знайдено службу PostgreSQL: {service_name} (Display: {line.split(':', 1)[1].strip()})")
                                break # Знайшли службу
                        except IndexError:
                            print(f"[DEBUG] Помилка парсингу SERVICE_NAME для рядка: {prev_line}")
                            continue
                if service_name:
                    break # Знайшли, виходимо

        if not service_name:
            print("[DEBUG] Не вдалося знайти службу PostgreSQL за DISPLAY_NAME. Спробуйте перевірити 'services.msc'.")

        return service_name

    except Exception as e:
        print(f"[DEBUG] Помилка під час пошуку імені служби: {e}")
        return None


def start_postgres():
    """Запуск PostgreSQL"""
    print("\n=== Спроба запуску PostgreSQL ===")
    try:
        if platform.system() == 'Windows':
            service_name = find_postgres_service_name()
            if not service_name:
                print("✗ Не вдалося автоматично визначити ім'я служби PostgreSQL для запуску.")
                print("  Переконайтесь, що PostgreSQL встановлено та ім'я служби містить 'postgresql'.")
                print("  Спробуйте запустити службу вручну через 'services.msc'.")
                return False

            # Перевіряємо, чи служба вже запущена перед спробою старту
            if check_postgres_running(): # Використовуємо оновлену функцію перевірки
                 print(f"✓ Служба PostgreSQL '{service_name}' вже працює.")
                 return True

            # Запускаємо знайдену службу
            cmd = ['sc', 'start', service_name]
            print(f"\n[DEBUG] Виконуємо команду: {' '.join(cmd)}")
            try:
                import locale
                encoding = locale.getpreferredencoding()
                # Використовуємо check_output для кращої обробки помилок
                output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, encoding=encoding, errors='replace')
                print(f"✓ Команда запуску служби PostgreSQL '{service_name}' виконана.")
                print(f"[DEBUG] Вивід команди запуску:\n{output}")
                print("Очікування стабілізації служби...")
                time.sleep(5) # Збільшено час очікування
                # Повторна перевірка статусу після спроби запуску
                if check_postgres_running():
                    print(f"✓ Служба PostgreSQL '{service_name}' успішно запущена та перевірена.")
                    return True
                else:
                    print(f"✗ Не вдалося підтвердити запуск служби '{service_name}' після команди start.")
                    return False
            except subprocess.CalledProcessError as e:
                # Перевіряємо, чи служба вже запущена (код помилки 1056)
                # Або якщо вивід містить повідомлення про вже запущений стан
                already_running_indicators = ['1056', 'already been started', 'уже запущен']
                if e.returncode == 1056 or any(indicator in e.output.lower() for indicator in already_running_indicators):
                    print(f"✓ Служба PostgreSQL '{service_name}' вже працює (виявлено під час спроби запуску).")
                    time.sleep(1)
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

        elif platform.system() == 'Linux':
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
    except Exception as e:
        import traceback
        print(f"ПОМИЛКА ЗАПУСКУ POSTGRESQL: {e}\nТрасування стеку:\n{traceback.format_exc()}")
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