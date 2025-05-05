# Головний файл запуску системи підтримки прийняття рішень ГУ НГУ

from database import setup_db
from data_processing import data_collector, scheduler
from analytics import data_analyzer
import subprocess
import sys
import os

def init_database():
    print("[INFO] Ініціалізація бази даних...")
    setup_db.main()

def start_data_processing():
    print("[INFO] Запуск збору та обробки даних...")
    data_collector.main()
    scheduler.main()

def start_analytics():
    print("[INFO] Запуск аналітичного модуля...")
    data_analyzer.main()

def start_dashboard():
    print("[INFO] Запуск дашборду...")
    dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard', 'app.py')
    subprocess.Popen([sys.executable, dashboard_path])

def main():
    init_database()
    start_data_processing()
    start_analytics()
    start_dashboard()
    print("[INFO] Система запущена. Веб-інтерфейс доступний у браузері.")

if __name__ == "__main__":
    main()# Головний файл запуску системи підтримки прийняття рішень ГУ НГУ

from database import setup_db
from data_processing import data_collector, scheduler
from analytics import data_analyzer
import subprocess
import sys
import os

def init_database():
    print("[INFO] Ініціалізація бази даних...")
    setup_db.main()

def start_data_processing():
    print("[INFO] Запуск збору та обробки даних...")
    data_collector.main()
    scheduler.main()

def start_analytics():
    print("[INFO] Запуск аналітичного модуля...")
    data_analyzer.main()

def start_dashboard():
    print("[INFO] Запуск дашборду...")
    dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard', 'app.py')
    subprocess.Popen([sys.executable, dashboard_path])

def main():
    init_database()
    start_data_processing()
    start_analytics()
    start_dashboard()
    print("[INFO] Система запущена. Веб-інтерфейс доступний у браузері.")

if __name__ == "__main__":
    main()