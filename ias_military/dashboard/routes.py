# Маршрути дашборду для інформаційно-аналітичної системи Національної гвардії України

from flask import Blueprint, render_template, request, jsonify, current_app
import json
import datetime
import sys
import os
from jinja2 import TemplateNotFound

# Додаємо шлях до батьківської директорії в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Імпортуємо аналітичний модуль
from api.analytics import NGUAnalytics

# Ініціалізуємо аналітичний модуль
analytics = NGUAnalytics()

dashboard = Blueprint('dashboard', __name__, template_folder='templates/dashboard')

@dashboard.route('/')
def index():
    try:
        system_data = {}  # TODO: отримати дані з бази або моделі
        return render_template('index.html', system_data=system_data)
    except TemplateNotFound:
        current_app.logger.error('Відсутній шаблон: index.html')
        return 'Шаблон не знайдено', 404

@dashboard.route('/threat-analysis')
def threat_analysis():
    try:
        system_data = {}  # TODO: отримати дані з бази або моделі
        return render_template('threat_analysis.html', system_data=system_data)
    except TemplateNotFound:
        current_app.logger.error('Відсутній шаблон: threat_analysis.html')
        return 'Шаблон аналізу загроз не знайдено', 404

@dashboard.route('/api/dashboard/predict-resources', methods=['POST'])
def predict_resources_dashboard():
    try:
        data = request.get_json()
        result = analytics.predict_resource_need(
            threat_level=data['threat_level'],
            region=data['region'],
            location=data['location'],
            status=data['status'],
            unit_type=data['unit_type'],
            personnel_count=data['personnel_count'],
            readiness_level=data.get('readiness_level', 3),
            incident_types={
                'Порушення громадського порядку': data.get('public_disorder', 0),
                'Терористична загроза': data.get('terrorist_threat', 0),
                'Диверсія': data.get('sabotage', 0),
                'Масові заворушення': data.get('mass_riots', 0),
                'Блокування об\'єктів': data.get('object_blocking', 0)
            },
            avg_severity=data.get('avg_severity', 0),
            total_casualties=data.get('total_casualties', 0),
            property_damage_count=data.get('property_damage_count', 0)
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Помилка при прогнозуванні ресурсів: {str(e)}'}), 500