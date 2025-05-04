# Маршрути для вдосконаленого дашборду
# Цей файл більше не використовується для реєстрації Blueprint або init_dash,
# оскільки інтеграція відбувається через DispatcherMiddleware у run.py

# Можна залишити для потенційних майбутніх маршрутів Flask, специфічних для цього дашборду,
# але наразі він порожній з точки зору функціональності інтеграції Dash.

# import sys
# import os
# from flask import Blueprint, render_template, current_app
# from jinja2 import TemplateNotFound

# # Додаємо шлях до батьківської директорії в sys.path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# # Створюємо Blueprint (закоментовано, оскільки не використовується)
# # improved_dashboard = Blueprint('improved_dashboard', __name__, template_folder='templates')

# # @improved_dashboard.route('/')
# # def index():
# #     """Головна сторінка вдосконаленого дашборду"""
# #     try:
# #         # Цей маршрут більше не потрібен, оскільки Dash обробляє свій шлях
# #         # return render_template('dashboard/improved_dashboard.html')
# #         pass # Або повернути щось інше, якщо цей Blueprint буде використовуватися
# #     except TemplateNotFound:
# #         current_app.logger.error('Відсутній шаблон: improved_dashboard.html')
# #         return 'Шаблон не знайдено', 404

# # Функція init_dash більше не потрібна
# # def init_dash(flask_app):
# #     pass