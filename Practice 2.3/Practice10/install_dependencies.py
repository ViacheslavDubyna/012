# Скрипт для встановлення необхідних бібліотек для роботи з нейронними мережами

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

def install_dependencies():
    print("\n=== Встановлення необхідних бібліотек для роботи з нейронними мережами ===\n")
    
    # Список необхідних бібліотек
    libraries = [
        "tensorflow",
        "matplotlib",
        "scikit-learn",
        "numpy",
        "pandas"
    ]
    
    # Встановлення кожної бібліотеки
    success = True
    for lib in libraries:
        print(f"\nВстановлення {lib}...")
        result = run_command(f"{sys.executable} -m pip install {lib}")
        
        if result == 0:
            print(f"{lib} успішно встановлено!")
        else:
            print(f"Виникла помилка при встановленні {lib}.")
            success = False
    
    return success

def verify_installations():
    print("\n=== Перевірка встановлених бібліотек ===\n")
    
    libraries_to_check = {
        "tensorflow": "tf",
        "matplotlib": "plt",
        "sklearn": "sklearn",
        "numpy": "np",
        "pandas": "pd"
    }
    
    all_installed = True
    
    for lib, alias in libraries_to_check.items():
        try:
            if lib == "tensorflow":
                import tensorflow as tf
                print(f"✓ {lib} успішно імпортовано! Версія: {tf.__version__}")
            elif lib == "matplotlib":
                import matplotlib.pyplot as plt
                print(f"✓ {lib} успішно імпортовано!")
            elif lib == "sklearn":
                import sklearn
                print(f"✓ {lib} успішно імпортовано! Версія: {sklearn.__version__}")
            elif lib == "numpy":
                import numpy as np
                print(f"✓ {lib} успішно імпортовано! Версія: {np.__version__}")
            elif lib == "pandas":
                import pandas as pd
                print(f"✓ {lib} успішно імпортовано! Версія: {pd.__version__}")
        except ImportError:
            print(f"✗ Не вдалося імпортувати {lib}. Перевірте, чи правильно він встановлений.")
            all_installed = False
        except Exception as e:
            print(f"✗ Помилка при перевірці {lib}: {e}")
            all_installed = False
    
    return all_installed

if __name__ == "__main__":
    print("=== Встановлення та перевірка бібліотек для роботи з нейронними мережами ===\n")
    
    # Встановлення бібліотек
    if install_dependencies():
        print("\nВсі бібліотеки успішно встановлено!")
    else:
        print("\nВиникли помилки при встановленні деяких бібліотек.")
    
    # Перевірка встановлення
    if verify_installations():
        print("\nВсі необхідні бібліотеки успішно встановлено та перевірено!")
    else:
        print("\nДеякі бібліотеки не вдалося перевірити. Перевірте помилки вище.")
    
    print("\n=== Завершено ===\n")
    print("Тепер ви можете запустити Jupyter Notebook та виконати завдання з нейронними мережами.")