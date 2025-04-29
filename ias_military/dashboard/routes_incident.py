# Маршрути для управління інцидентами для інформаційно-аналітичної системи Національної гвардії України

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

@dashboard.route('/incident-management')
def incident_management():
    """Сторінка управління інцидентами"""
    # Отримуємо дані про інциденти
    incidents_df = analytics.get_incident_data()
    
    # Перетворюємо дані для відображення на графіках
    incidents_by_type = incidents_df.groupby('type').size().to_dict()
    incidents_by_severity = incidents_df.groupby('severity').size().to_dict()
    
    # Отримуємо тренди інцидентів
    trends = analytics.analyze_incident_trends(days=30)
    
    return render_template(
        'incident_management.html',
        incidents_by_type=json.dumps(incidents_by_type),
        incidents_by_severity=json.dumps(incidents_by_severity),
        trends=json.dumps(trends),
        incidents=incidents_df.to_dict('records')
    )

@dashboard.route('/api/dashboard/incidents', methods=['GET'])
def get_incidents():
    """API ендпоінт для отримання списку інцидентів"""
    incidents_df = analytics.get_incident_data()
    return jsonify(incidents_df.to_dict('records'))

@dashboard.route('/api/dashboard/incidents/<int:incident_id>', methods=['GET'])
def get_incident(incident_id):
    """API ендпоінт для отримання інформації про інцидент"""
    incident = analytics.session.query(analytics.Incident).filter_by(id=incident_id).first()
    if not incident:
        return jsonify({'error': 'Інцидент не знайдено'}), 404
    
    return jsonify({
        'id': incident.id,
        'type': incident.type,
        'subtype': incident.subtype,
        'location': incident.location,
        'timestamp': incident.timestamp.isoformat(),
        'severity': incident.severity,
        'status': incident.status,
        'casualties': incident.casualties,
        'property_damage': incident.property_damage,
        'situation_id': incident.situation_id
    })

@dashboard.route('/incidents/<int:incident_id>')
def incident_details(incident_id):
    """Сторінка з детальною інформацією про інцидент"""
    incident = analytics.session.query(analytics.Incident).filter_by(id=incident_id).first()
    if not incident:
        return redirect(url_for('dashboard.incident_management'))
    
    return render_template(
        'incident_details.html',
        incident={
            'id': incident.id,
            'type': incident.type,
            'subtype': incident.subtype,
            'location': incident.location,
            'timestamp': incident.timestamp.isoformat(),
            'severity': incident.severity,
            'status': incident.status,
            'casualties': incident.casualties,
            'property_damage': incident.property_damage,
            'situation_id': incident.situation_id
        }
    )