# Скрипт для встановлення та перевірки TensorFlow

import subprocess
import sys
import os

def run_command(command):
    print(f"Виконую команду: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout.decode('utf-8'))
    if stderr:
        print(f"Помилка: {stderr.decode('utf-8')}")
    return process.returncode

def enable_long_paths():
    print("Налаштування підтримки довгих шляхів у Windows...")
    # Команда для включення підтримки довгих шляхів у Windows
    command = 'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\FileSystem" /v "LongPathsEnabled" /t REG_DWORD /d 1 /f'
    try:
        # Спроба виконати команду з правами адміністратора
        result = run_command(command)
        if result == 0:
            print("Підтримка довгих шляхів успішно включена!")
            return True
        else:
            print("Не вдалося включити підтримку довгих шляхів. Можливо, потрібні права адміністратора.")
            print("Будь ласка, запустіть цей скрипт з правами адміністратора або виконайте команду вручну:")
            print(command)
            return False
    except Exception as e:
        print(f"Помилка при налаштуванні довгих шляхів: {e}")
        return False

def install_tensorflow():
    print("\n=== Встановлення TensorFlow ===")
    # Спочатку очистимо кеш pip
    run_command(f"{sys.executable} -m pip cache purge")
    
    # Видалимо TensorFlow, якщо він вже встановлений
    run_command(f"{sys.executable} -m pip uninstall -y tensorflow")
    
    # Встановимо TensorFlow
    result = run_command(f"{sys.executable} -m pip install tensorflow")
    
    if result == 0:
        print("\nTensorFlow успішно встановлено!")
        return True
    else:
        print("\nВиникла помилка при встановленні TensorFlow.")
        return False

def verify_tensorflow():
    print("\n=== Перевірка встановлення TensorFlow ===")
    try:
        # Спробуємо імпортувати TensorFlow
        import tensorflow as tf
        print(f"TensorFlow успішно імпортовано! Версія: {tf.__version__}")
        
        # Виведемо інформацію про доступні пристрої
        print("\nДоступні пристрої:")
        for device in tf.config.list_physical_devices():
            print(f" - {device}")
            
        # Проста операція для перевірки
        print("\nПеревірка роботи TensorFlow:")
        a = tf.constant([[1, 2], [3, 4]])
        b = tf.constant([[5, 6], [7, 8]])
        c = tf.matmul(a, b)
        print(f"Результат множення матриць:\n{c}")
        
        return True
    except ImportError:
        print("Не вдалося імпортувати TensorFlow. Перевірте, чи правильно він встановлений.")
        return False
    except Exception as e:
        print(f"Помилка при перевірці TensorFlow: {e}")
        return False

def main():
    print("=== Програма встановлення та перевірки TensorFlow ===")
    
    # Перевіримо, чи увімкнена підтримка довгих шляхів
    enable_long_paths()
    
    # Встановимо TensorFlow
    if install_tensorflow():
        # Перевіримо встановлення
        verify_tensorflow()
    
    print("\n=== Завершено ===")
    print("Якщо ви використовуєте Jupyter Notebook, перезапустіть ядро для застосування змін.")

if __name__ == "__main__":
    main()