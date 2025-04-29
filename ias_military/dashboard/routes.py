# Маршрути дашборду для інформаційно-аналітичної системи Національної гвардії України

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

@dashboard.route('/')
def index():
    """Головна сторінка дашборду"""
    return render_template('index.html')

@dashboard.route('/threat-analysis')
def threat_analysis():
    """Сторінка аналізу загроз"""
    # Отримуємо дані про оперативну обстановку
    situations_df = analytics.get_situation_data()
    
    # Перетворюємо дані для відображення на графіках
    threat_by_region = situations_df.groupby('region')['threat_level'].mean().to_dict()
    threat_by_status = situations_df.groupby('status')['threat_level'].mean().to_dict()
    
    # Отримуємо дані про інциденти
    incidents_df = analytics.get_incident_data()
    incident_by_type = incidents_df.groupby('type').size().to_dict()
    
    # Отримуємо тренди інцидентів
    trends = analytics.analyze_incident_trends(days=30)
    
    return render_template(
        'threat_analysis.html',
        threat_by_region=json.dumps(threat_by_region),
        threat_by_status=json.dumps(threat_by_status),
        incident_by_type=json.dumps(incident_by_type),
        trends=json.dumps(trends)
    )

@dashboard.route('/resource-management')
def resource_management():
    """Сторінка управління ресурсами"""
    # Отримуємо дані про ресурси
    resources_df = analytics.get_resource_data()
    
    # Перетворюємо дані для відображення на графіках
    resources_by_type = resources_df.groupby('type')['quantity'].sum().to_dict()
    resources_by_status = resources_df.groupby('status')['quantity'].sum().to_dict()
    
    # Отримуємо дані про підрозділи
    units_df = analytics.session.query(analytics.session.query(analytics.NGUUnit).statement, analytics.engine)
    
    return render_template(
        'resource_management.html',
        resources_by_type=json.dumps(resources_by_type),
        resources_by_status=json.dumps(resources_by_status),
        units=units_df.to_dict('records')
    )

@dashboard.route('/decision-effectiveness')
def decision_effectiveness():
    """Сторінка аналізу ефективності рішень"""
    # Отримуємо дані про ефективність рішень
    effectiveness = analytics.evaluate_decision_effectiveness(days=30)
    
    # Отримуємо дані про рішення
    decisions_df = analytics.get_decision_data()
    
    return render_template(
        'decision_effectiveness.html',
        effectiveness=json.dumps(effectiveness),
        decisions=decisions_df.to_dict('records')
    )

@dashboard.route('/prediction-tools')
def prediction_tools():
    """Сторінка інструментів прогнозування"""
    # Отримуємо дані про підрозділи для форми
    units_df = analytics.session.query(analytics.session.query(analytics.NGUUnit).statement, analytics.engine)
    
    return render_template(
        'prediction_tools.html',
        units=units_df.to_dict('records')
    )

@dashboard.route('/api/dashboard/predict-threat', methods=['POST'])
def predict_threat_dashboard():
    """API ендпоінт для прогнозування загроз з дашборду"""
    data = request.get_json()
    
    # Перевіряємо наявність необхідних полів
    required_fields = ['region', 'location', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Відсутнє поле {field}'}), 400
    
    # Перевіряємо, чи є модель прогнозування загроз
    if 'threat_prediction' not in analytics.models:
        # Якщо моделі немає, навчаємо її
        try:
            analytics.train_threat_prediction_model()
        except Exception as e:
            return jsonify({'error': f'Помилка при навчанні моделі: {str(e)}'}), 500
    
    # Створюємо DataFrame з вхідними даними
    import pandas as pd
    import numpy as np
    
    # Отримуємо поточний час
    now = datetime.datetime.now()
    
    input_data = {
        'hour': [now.hour],
        'day': [now.day],
        'month': [now.month],
        'day_of_week': [now.weekday()],
        'avg_severity': [data.get('avg_severity', 0)],
        'total_casualties': [data.get('total_casualties', 0)],
        'property_damage_count': [data.get('property_damage_count', 0)],
        'readiness_level': [data.get('readiness_level', 3)],
        'region': [data['region']],
        'location': [data['location']],
        'status': [data['status']]
    }
    
    # Додаємо дані про типи інцидентів
    incident_types = {
        'Порушення громадського порядку': data.get('public_disorder', 0),
        'Терористична загроза': data.get('terrorist_threat', 0),
        'Диверсія': data.get('sabotage', 0),
        'Масові заворушення': data.get('mass_riots', 0),
        'Блокування об\'єктів': data.get('object_blocking', 0)
    }
    
    for incident_type, count in incident_types.items():
        input_data[incident_type] = [count]
    
    df = pd.DataFrame(input_data)
    
    # Прогнозуємо рівень загрози
    try:
        prediction_proba = analytics.models['threat_prediction'].predict_proba(df)[0]
        prediction = analytics.models['threat_prediction'].predict(df)[0]
        
        # Зберігаємо прогноз у базі даних
        from database.models import Prediction
        
        prediction_obj = Prediction(
            timestamp=now,
            prediction_type='Загроза',
            location=data['location'],
            region=data['region'],
            prediction_value=float(prediction),
            confidence=float(prediction_proba[1]) if prediction == 1 else float(prediction_proba[0]),
            description=f"Прогноз рівня загрози для регіону {data['region']} ({data['location']}) зі статусом {data['status']}",
            threat_type='Високий рівень загрози' if prediction == 1 else 'Низький рівень загрози'
        )
        analytics.session.add(prediction_obj)
        analytics.session.commit()
        
        return jsonify({
            'prediction': int(prediction),
            'probability': float(prediction_proba[1]),
            'prediction_id': prediction_obj.id,
            'threat_level': 'Високий' if prediction == 1 else 'Низький'
        })
    except Exception as e:
        return jsonify({'error': f'Помилка при прогнозуванні: {str(e)}'}), 500

@dashboard.route('/api/dashboard/predict-resources', methods=['POST'])
def predict_resources_dashboard():
    """API ендпоінт для прогнозування ресурсів з дашборду"""
    data = request.get_json()
    
    # Перевіряємо наявність необхідних полів
    required_fields = ['threat_level', 'region', 'location', 'status', 'unit_type', 'personnel_count']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Відсутнє поле {field}'}), 400
    
    # Прогнозуємо потреби у ресурсах
    try:
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