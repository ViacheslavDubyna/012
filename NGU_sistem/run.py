#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Головний файл запуску інформаційно-аналітичної системи НГУ
"""

import os
import sys
from flask import Flask, render_template, redirect, url_for

# Додаємо шлях до проекту в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Імпортуємо модулі системи
from config.config import Config
from api.routes import api_bp
from dashboard.routes import dashboard_bp

def create_app(config=Config):
    """Створення та налаштування Flask додатку"""
    app = Flask(__name__, 
                template_folder='dashboard/templates',
                static_folder='dashboard/static')
    
    # Застосовуємо конфігурацію
    app.config.from_object(config)
    
    # Реєструємо blueprint'и
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    
    # Головна сторінка - перенаправлення на дашборд
    @app.route('/')
    def index():
        return redirect(url_for('dashboard.index'))
    
    return app

def main():
    """Головна функція запуску системи"""
    app = create_app()
    print("Інформаційно-аналітична система НГУ запущена!")
    print("Дашборд доступний за адресою: http://localhost:5100/dashboard")
    print("API доступне за адресою: http://localhost:5100/api")
    app.run(host='0.0.0.0', port=5100, debug=True)

if __name__ == '__main__':
    main()