# Маршрути для управління підрозділами для інформаційно-аналітичної системи Національної гвардії України

from flask import render_template, request, redirect, url_for, jsonify
from . import dashboard
import json
import datetime
import sys
import os

# Додаємо шлях до батьківської директорії в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Імпортуємо аналітичний модуль
from api.analytics import NGUAnalytics

# Ініціалізуємо аналітичний модуль
analytics = NGUAnalytics()

@dashboard.route('/unit-management')
def unit_management():
    """Сторінка управління підрозділами"""
    # Отримуємо дані про підрозділи
    units_df = analytics.session.query(analytics.session.query(analytics.NGUUnit).statement, analytics.engine)
    
    # Перетворюємо дані для відображення на графіках
    units_by_type = units_df.groupby('type').size().to_dict()
    units_by_region = units_df.groupby('region').size().to_dict()
    
    return render_template(
        'unit_management.html',
        units_by_type=json.dumps(units_by_type),
        units_by_region=json.dumps(units_by_region),
        units=units_df.to_dict('records')
    )

@dashboard.route('/api/dashboard/units', methods=['GET'])
def get_units():
    """API ендпоінт для отримання списку підрозділів"""
    units_df = analytics.session.query(analytics.session.query(analytics.NGUUnit).statement, analytics.engine)
    return jsonify(units_df.to_dict('records'))

@dashboard.route('/api/dashboard/units/<int:unit_id>', methods=['GET'])
def get_unit(unit_id):
    """API ендпоінт для отримання інформації про підрозділ"""
    unit = analytics.session.query(analytics.NGUUnit).filter_by(id=unit_id).first()
    if not unit:
        return jsonify({'error': 'Підрозділ не знайдено'}), 404
    
    return jsonify({
        'id': unit.id,
        'name': unit.name,
        'type': unit.type,
        'region': unit.region,
        'location': unit.location,
        'personnel_count': unit.personnel_count,
        'readiness_level': unit.readiness_level,
        'status': unit.status
    })