# Конфігурація для інформаційно-аналітичної системи Національної гвардії України

import os

# Налаштування бази даних
DB_CONFIG = {
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'database': 'ngu_ias'
}

# Формування URL для підключення до бази даних
DB_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# Налаштування веб-сервера
SERVER_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True
}

# Шляхи до директорій
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Створення директорії для збереження моделей, якщо вона не існує
if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

# Налаштування для аналітичного модуля
ANALYTICS_CONFIG = {
    'models_dir': MODELS_DIR,
    'prediction_confidence_threshold': 0.7,
    'resource_allocation_threshold': 0.5
}