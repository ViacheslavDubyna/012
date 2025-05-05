#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Планувальник завдань для автоматичного збору даних через певні проміжки часу.
"""

import os
import sys
import time
import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from data_collector import run_data_collection

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('scheduler')

# Клас планувальника завдань
class DataCollectionScheduler:
    def __init__(self, interval_minutes=30):
        self.interval_minutes = interval_minutes
        self.scheduler = BackgroundScheduler()
        logger.info(f"Ініціалізовано планувальник з інтервалом {interval_minutes} хвилин")
    
    def start(self):
        """
        Запуск планувальника завдань
        """
        try:
            # Додавання завдання збору даних до планувальника
            self.scheduler.add_job(
                run_data_collection,
                IntervalTrigger(minutes=self.interval_minutes),
                id='data_collection_job',
                name='Збір та обробка даних',
                replace_existing=True
            )
            
            # Запуск планувальника
            self.scheduler.start()
            logger.info("Планувальник завдань успішно запущено")
            
            # Виконання першого збору даних відразу після запуску
            logger.info("Виконання першого збору даних...")
            run_data_collection()
            
            return True
        except Exception as e:
            logger.error(f"Помилка при запуску планувальника завдань: {e}")
            return False
    
    def stop(self):
        """
        Зупинка планувальника завдань
        """
        try:
            self.scheduler.shutdown()
            logger.info("Планувальник завдань зупинено")
            return True
        except Exception as e:
            logger.error(f"Помилка при зупинці планувальника завдань: {e}")
            return False
    
    def change_interval(self, new_interval_minutes):
        """
        Зміна інтервалу збору даних
        """
        try:
            self.interval_minutes = new_interval_minutes
            
            # Видалення існуючого завдання
            self.scheduler.remove_job('data_collection_job')
            
            # Додавання нового завдання з новим інтервалом
            self.scheduler.add_job(
                run_data_collection,
                IntervalTrigger(minutes=self.interval_minutes),
                id='data_collection_job',
                name='Збір та обробка даних',
                replace_existing=True
            )
            
            logger.info(f"Інтервал збору даних змінено на {new_interval_minutes} хвилин")
            return True
        except Exception as e:
            logger.error(f"Помилка при зміні інтервалу збору даних: {e}")
            return False

# Функція для запуску планувальника як сервісу
def run_scheduler_service(interval_minutes=30):
    """
    Запуск планувальника як сервісу
    """
    logger.info("Запуск сервісу планувальника збору даних...")
    
    scheduler = DataCollectionScheduler(interval_minutes)
    if scheduler.start():
        try:
            # Утримання основного потоку активним
            while True:
                time.sleep(60)
        except (KeyboardInterrupt, SystemExit):
            scheduler.stop()
            logger.info("Сервіс планувальника збору даних зупинено користувачем")
    else:
        logger.error("Не вдалося запустити сервіс планувальника збору даних")

# Головна функція
def main():
    # Отримання інтервалу з аргументів командного рядка (за замовчуванням 30 хвилин)
    interval = 30
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
        except ValueError:
            logger.warning(f"Неправильний формат інтервалу: {sys.argv[1]}. Використовується значення за замовчуванням: 30 хвилин")
    
    run_scheduler_service(interval)

if __name__ == "__main__":
    main()