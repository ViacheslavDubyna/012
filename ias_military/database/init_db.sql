-- Скрипт для ініціалізації бази даних PostgreSQL для інформаційно-аналітичної системи Національної гвардії України

-- Створення бази даних, якщо вона не існує
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'ngu_ias') THEN
        CREATE DATABASE ngu_ias;
    END IF;
END
$$;

-- Підключення до бази даних ngu_ias
\c ngu_ias;

-- Створення розширень, якщо потрібно
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Коментар до бази даних
COMMENT ON DATABASE ngu_ias IS 'База даних для інформаційно-аналітичної системи Національної гвардії України';

-- Примітка: Таблиці будуть створені автоматично за допомогою SQLAlchemy ORM
-- при запуску команди python run.py init_db