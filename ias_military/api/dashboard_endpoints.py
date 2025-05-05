# API-ендпоінти для дашборду інформаційно-аналітичної системи Національної гвардії України

from flask import jsonify, request
from . import app
from .analytics import NGUAnalytics
from .analytics_ai import ai_predictor
import datetime
import pandas as pd
import random

# Ініціалізуємо аналітичний модуль
analytics = NGUAnalytics()

@app.route('/dashboard/statistics', methods=['GET'])
def get_dashboard_statistics():
    """Отримання загальної статистики для головної сторінки дашборду"""
    try:
        # Отримуємо дані з бази даних
        units_count = analytics.session.query(analytics.NGUUnit).count()
        
        resources_count = analytics.session.query(analytics.Resource)\
            .filter(analytics.Resource.status == 'Доступний')\
            .count()
        
        # Отримуємо дату 30 днів тому
        thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
        
        incidents_count = analytics.session.query(analytics.Incident)\
            .filter(analytics.Incident.timestamp >= thirty_days_ago)\
            .count()
        
        critical_situations_count = analytics.session.query(analytics.OperationalSituation)\
            .filter(analytics.OperationalSituation.status.in_(['Критична', 'Надзвичайна']))\
            .count()
        
        return jsonify({
            'units_count': units_count,
            'resources_count': resources_count,
            'incidents_count': incidents_count,
            'critical_situations_count': critical_situations_count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/incidents/recent', methods=['GET'])
def get_recent_incidents():
    """Отримання останніх інцидентів"""
    try:
        # Отримуємо останні 5 інцидентів
        incidents = analytics.session.query(analytics.Incident)\
            .order_by(analytics.Incident.timestamp.desc())\
            .limit(5)\
            .all()
        
        result = []
        for incident in incidents:
            result.append({
                'id': incident.id,
                'type': incident.type,
                'subtype': incident.subtype,
                'location': incident.location,
                'timestamp': incident.timestamp.isoformat(),
                'severity': incident.severity,
                'status': incident.status
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analytics/threat-level-history', methods=['GET'])
def get_threat_level_history():
    """Отримання історії рівня загрози"""
    try:
        # Отримуємо дані про оперативну обстановку за останні 30 днів
        thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
        
        situations = analytics.session.query(
            analytics.OperationalSituation.timestamp,
            analytics.OperationalSituation.threat_level
        ).filter(
            analytics.OperationalSituation.timestamp >= thirty_days_ago
        ).order_by(
            analytics.OperationalSituation.timestamp
        ).all()
        
        # Групуємо дані за датами
        df = pd.DataFrame([(s.timestamp.date(), s.threat_level) for s in situations], 
                          columns=['date', 'threat_level'])
        
        daily_avg = df.groupby('date')['threat_level'].mean().reset_index()
        
        return jsonify({
            'dates': [d.strftime('%d.%m.%Y') for d in daily_avg['date']],
            'threat_levels': daily_avg['threat_level'].tolist()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/resources/distribution', methods=['GET'])
def get_resources_distribution():
    """Отримання даних про розподіл ресурсів для візуалізації"""
    try:
        # Отримуємо дані про ресурси з бази даних
        resources = analytics.session.query(analytics.Resource).all()
        
        # Підготовка даних для відповіді
        result = {
            'resources': [],
            'by_type': {},
            'by_status': {}
        }
        
        # Формуємо список ресурсів з відсотком використання
        for resource in resources:
            # Розраховуємо відсоток використання (для прикладу)
            usage_percentage = random.randint(30, 95)  # В реальній системі тут буде реальний розрахунок
            
            result['resources'].append({
                'id': resource.id,
                'name': f"{resource.type} - {resource.subtype}",
                'type': resource.type,
                'subtype': resource.subtype,
                'quantity': resource.quantity,
                'status': resource.status,
                'usage_percentage': usage_percentage
            })
            
            # Групуємо за типом
            if resource.type not in result['by_type']:
                result['by_type'][resource.type] = {
                    'count': 0,
                    'percentage': 0
                }
            result['by_type'][resource.type]['count'] += 1
            
            # Групуємо за статусом
            if resource.status not in result['by_status']:
                result['by_status'][resource.status] = {
                    'count': 0,
                    'percentage': 0
                }
            result['by_status'][resource.status]['count'] += 1
        
        # Розраховуємо відсотки для типів
        total_resources = len(resources)
        for resource_type in result['by_type']:
            result['by_type'][resource_type]['percentage'] = round(
                (result['by_type'][resource_type]['count'] / total_resources) * 100, 1
            ) if total_resources > 0 else 0
        
        # Розраховуємо відсотки для статусів
        for status in result['by_status']:
            result['by_status'][status]['percentage'] = round(
                (result['by_status'][status]['count'] / total_resources) * 100, 1
            ) if total_resources > 0 else 0
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
def get_resource_distribution():
    """Отримання розподілу ресурсів за типами"""
    try:
        # Отримуємо дані про ресурси
        resources = analytics.session.query(
            analytics.Resource.type,
            analytics.func.sum(analytics.Resource.quantity).label('total')
        ).group_by(
            analytics.Resource.type
        ).all()
        
        labels = [r.type for r in resources]
        values = [r.total for r in resources]
        
        return jsonify({
            'labels': labels,
            'values': values
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analytics/predictions', methods=['GET'])
def get_ai_predictions():
    """Отримання прогнозів AI-моделей"""
    try:
        # Отримуємо останні прогнози з бази даних
        predictions = analytics.session.query(analytics.Prediction)\
            .order_by(analytics.Prediction.timestamp.desc())\
            .limit(3)\
            .all()
        
        result = []
        for prediction in predictions:
            result.append({
                'id': prediction.id,
                'type': prediction.prediction_type,
                'region': prediction.region,
                'location': prediction.location,
                'value': prediction.prediction_value,
                'confidence': prediction.confidence,
                'description': prediction.description,
                'timestamp': prediction.timestamp.isoformat()
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/situations/map-data', methods=['GET'])
def get_map_data():
    """Отримання даних для карти оперативної обстановки"""
    try:
        # Отримуємо дані про оперативну обстановку
        situations = analytics.session.query(analytics.OperationalSituation)\
            .order_by(analytics.OperationalSituation.timestamp.desc())\
            .limit(50)\
            .all()
        
        result = []
        for situation in situations:
            # Генеруємо випадкові координати для демонстрації
            # В реальній системі тут будуть справжні координати
            lat = random.uniform(44.0, 52.0)
            lng = random.uniform(22.0, 40.0)
            
            result.append({
                'id': situation.id,
                'location': situation.location,
                'region': situation.region,
                'status': situation.status,
                'threat_level': situation.threat_level,
                'timestamp': situation.timestamp.isoformat(),
                'coordinates': f"{lat:.6f}, {lng:.6f}"
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/units', methods=['GET'])
def get_units():
    """Отримання списку підрозділів НГУ"""
    try:
        units = analytics.session.query(analytics.NGUUnit).all()
        
        result = []
        for unit in units:
            result.append({
                'id': unit.id,
                'name': unit.name,
                'unit_type': unit.unit_type,
                'location': unit.location,
                'region': unit.region,
                'personnel_count': unit.personnel_count,
                'readiness_level': unit.readiness_level
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/resources', methods=['GET'])
def get_resources():
    """Отримання списку ресурсів"""
    try:
        # Отримуємо параметри фільтрації
        unit_id = request.args.get('unit_id')
        resource_type = request.args.get('type')
        status = request.args.get('status')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Формуємо запит з фільтрами
        query = analytics.session.query(analytics.Resource)\
            .join(analytics.NGUUnit, analytics.Resource.unit_id == analytics.NGUUnit.id)
        
        if unit_id:
            query = query.filter(analytics.Resource.unit_id == unit_id)
        
        if resource_type:
            query = query.filter(analytics.Resource.type == resource_type)
        
        if status:
            query = query.filter(analytics.Resource.status == status)
        
        # Пагінація
        total = query.count()
        total_pages = (total + per_page - 1) // per_page
        
        resources = query.offset((page - 1) * per_page).limit(per_page).all()
        
        result = []
        for resource in resources:
            result.append({
                'id': resource.id,
                'type': resource.type,
                'subtype': resource.subtype,
                'quantity': resource.quantity,
                'status': resource.status,
                'location': resource.location,
                'unit_id': resource.unit_id,
                'unit_name': resource.unit.name,
                'last_updated': resource.last_updated.isoformat()
            })
        
        return jsonify({
            'resources': result,
            'total': total,
            'total_pages': total_pages,
            'current_page': page
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/resources-charts-data', methods=['GET'])
def get_resources_charts_data():
    """Отримання даних для графіків розподілу ресурсів"""
    try:
        # Розподіл за типами
        by_type = analytics.session.query(
            analytics.Resource.type,
            analytics.func.sum(analytics.Resource.quantity).label('total')
        ).group_by(
            analytics.Resource.type
        ).all()
        
        # Розподіл за статусом
        by_status = analytics.session.query(
            analytics.Resource.status,
            analytics.func.sum(analytics.Resource.quantity).label('total')
        ).group_by(
            analytics.Resource.status
        ).all()
        
        return jsonify({
            'by_type': {
                'labels': [r.type for r in by_type],
                'values': [r.total for r in by_type]
            },
            'by_status': {
                'labels': [r.status for r in by_status],
                'values': [r.total for r in by_status]
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/resource-allocations', methods=['GET'])
def get_resource_allocations():
    """Отримання списку розподілів ресурсів"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Формуємо запит
        query = analytics.session.query(analytics.ResourceAllocation)\
            .join(analytics.Resource, analytics.ResourceAllocation.resource_id == analytics.Resource.id)\
            .join(analytics.OperationalSituation, analytics.ResourceAllocation.situation_id == analytics.OperationalSituation.id)
        
        # Пагінація
        total = query.count()
        total_pages = (total + per_page - 1) // per_page
        
        allocations = query.offset((page - 1) * per_page).limit(per_page).all()
        
        result = []
        for allocation in allocations:
            result.append({
                'id': allocation.id,
                'resource_id': allocation.resource_id,
                'resource_name': f"{allocation.resource.type} - {allocation.resource.subtype}",
                'situation_id': allocation.situation_id,
                'situation_location': allocation.situation.location,
                'quantity_allocated': allocation.quantity_allocated,
                'allocation_time': allocation.allocation_time.isoformat(),
                'allocation_status': allocation.allocation_status,
                'priority': allocation.priority,
                'notes': allocation.notes
            })
        
        return jsonify({
            'allocations': result,
            'total': total,
            'total_pages': total_pages,
            'current_page': page
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/situations', methods=['GET'])
def get_situations():
    """Отримання списку оперативних ситуацій"""
    try:
        situations = analytics.session.query(analytics.OperationalSituation)\
            .order_by(analytics.OperationalSituation.timestamp.desc())\
            .limit(50)\
            .all()
        
        result = []
        for situation in situations:
            result.append({
                'id': situation.id,
                'location': situation.location,
                'region': situation.region,
                'status': situation.status,
                'threat_level': situation.threat_level,
                'timestamp': situation.timestamp.isoformat(),
                'description': situation.description,
                'unit_id': situation.unit_id
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500