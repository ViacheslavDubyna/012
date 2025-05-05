# Маршрути API для інформаційно-аналітичної системи Національної гвардії України

from flask import Blueprint, request, jsonify, current_app
from api.analytics import NGUAnalytics

app = Blueprint('api', __name__)
analytics = NGUAnalytics()

# Прогнозування рівня загрози
@app.route('/api/analytics/threat-prediction', methods=['POST'])
def threat_prediction():
    """Ендпоінт для прогнозування рівня загрози"""
    data = request.get_json()
    
    # Перевіряємо наявність необхідних полів
    required_fields = ['region', 'location', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Відсутнє поле {field}'}), 400
    
    # Отримуємо додаткові параметри
    hour = data.get('hour', 12)
    day = data.get('day', 15)
    month = data.get('month', 6)
    day_of_week = data.get('day_of_week', 3)
    readiness_level = data.get('readiness_level', 3)
    
    # Отримуємо дані про інциденти
    incident_types = {
        'Порушення громадського порядку': data.get('public_disorder', 0),
        'Терористична загроза': data.get('terrorist_threat', 0),
        'Диверсія': data.get('sabotage', 0),
        'Масові заворушення': data.get('mass_riots', 0),
        'Блокування об\'єктів': data.get('object_blocking', 0)
    }
    
    avg_severity = data.get('avg_severity', 0)
    total_casualties = data.get('total_casualties', 0)
    property_damage_count = data.get('property_damage_count', 0)
    
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
    
    input_data = {
        'hour': [hour],
        'day': [day],
        'month': [month],
        'day_of_week': [day_of_week],
        'avg_severity': [avg_severity],
        'total_casualties': [total_casualties],
        'property_damage_count': [property_damage_count],
        'readiness_level': [readiness_level],
        'region': [data['region']],
        'location': [data['location']],
        'status': [data['status']]
    }
    
    # Додаємо дані про типи інцидентів
    for incident_type, count in incident_types.items():
        input_data[incident_type] = [count]
    
    df = pd.DataFrame(input_data)
    
    # Прогнозуємо рівень загрози
    try:
        prediction_proba = analytics.models['threat_prediction'].predict_proba(df)[0]
        prediction = analytics.models['threat_prediction'].predict(df)[0]
        
        # Зберігаємо прогноз у базі даних
        from database.models import Prediction
        import datetime
        
        prediction_obj = Prediction(
            timestamp=datetime.datetime.now(),
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

# Прогнозування потреби у ресурсах
@app.route('/api/analytics/resource-prediction', methods=['POST'])
def resource_prediction():
    """Ендпоінт для прогнозування потреб у ресурсах"""
    data = request.get_json()
    
    # Перевіряємо наявність необхідних полів
    required_fields = ['threat_level', 'region', 'location', 'status', 'unit_type', 'personnel_count']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Відсутнє поле {field}'}), 400
    
    # Отримуємо додаткові параметри
    readiness_level = data.get('readiness_level', 3)
    avg_severity = data.get('avg_severity', 0)
    total_casualties = data.get('total_casualties', 0)
    property_damage_count = data.get('property_damage_count', 0)
    
    # Отримуємо дані про інциденти
    incident_types = {
        'Порушення громадського порядку': data.get('public_disorder', 0),
        'Терористична загроза': data.get('terrorist_threat', 0),
        'Диверсія': data.get('sabotage', 0),
        'Масові заворушення': data.get('mass_riots', 0),
        'Блокування об\'єктів': data.get('object_blocking', 0)
    }
    
    # Прогнозуємо потреби у ресурсах
    try:
        result = analytics.predict_resource_need(
            threat_level=data['threat_level'],
            region=data['region'],
            location=data['location'],
            status=data['status'],
            unit_type=data['unit_type'],
            personnel_count=data['personnel_count'],
            readiness_level=readiness_level,
            incident_types=incident_types,
            avg_severity=avg_severity,
            total_casualties=total_casualties,
            property_damage_count=property_damage_count
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Помилка при прогнозуванні ресурсів: {str(e)}'}), 500

# Тренди інцидентів
@app.route('/api/analytics/incident-trends', methods=['GET'])
def incident_trends():
    """Ендпоінт для отримання трендів інцидентів"""
    days = request.args.get('days', default=30, type=int)
    
    try:
        trends = analytics.analyze_incident_trends(days=days)
        return jsonify(trends)
    except Exception as e:
        return jsonify({'error': f'Помилка при аналізі трендів: {str(e)}'}), 500

# Ефективність прийняття рішень
@app.route('/api/analytics/decision-effectiveness', methods=['GET'])
def decision_effectiveness():
    """Ендпоінт для отримання ефективності рішень"""
    days = request.args.get('days', default=30, type=int)
    
    try:
        effectiveness = analytics.evaluate_decision_effectiveness(days=days)
        return jsonify(effectiveness)
    except Exception as e:
        return jsonify({'error': f'Помилка при оцінці ефективності: {str(e)}'}), 500

# Тренування моделей
@app.route('/api/analytics/train-models', methods=['POST'])
def train_models():
    """Ендпоінт для навчання моделей"""
    try:
        threat_model, accuracy, report = analytics.train_threat_prediction_model()
        resource_model, rmse = analytics.train_resource_need_model()
        
        # Зберігаємо моделі
        analytics.save_models()
        
        return jsonify({
            'status': 'success',
            'threat_model_accuracy': float(accuracy),
            'resource_model_rmse': float(rmse)
        })
    except Exception as e:
        return jsonify({'error': f'Помилка при навчанні моделей: {str(e)}'}), 500

# Завантаження моделей
@app.route('/api/analytics/load-models', methods=['POST'])
def load_models():
    """Ендпоінт для завантаження моделей"""
    try:
        success = analytics.load_models()
        
        if success:
            return jsonify({'status': 'success', 'message': 'Моделі успішно завантажені'})
        else:
            return jsonify({'status': 'error', 'message': 'Не вдалося завантажити моделі'}), 404
    except Exception as e:
        return jsonify({'error': f'Помилка при завантаженні моделей: {str(e)}'}), 500