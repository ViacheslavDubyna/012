from flask import Flask, render_template, jsonify, request
import sys
import os
import json
import random
from datetime import datetime, timedelta

# Додавання шляхів до модулів аналітики та AI-моделей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'analytics')))
from data_analyzer import run_data_analysis

# Спроба імпортувати AI-моделі, якщо вони доступні
try:
    from analytics.ai_models import predict_threats, simulate_scenario
    ai_models_available = True
except ImportError:
    ai_models_available = False
    print("[WARNING] AI-моделі недоступні. Буде використано імітаційні дані.")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analytics')
def analytics_api():
    # Отримання аналітичних даних
    results = run_data_analysis(30)
    
    # Для серіалізації DataFrame/Series у JSON
    def serialize(obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict(orient='records')
        elif hasattr(obj, 'tolist'):
            return obj.tolist()
        return obj
    
    # Базові результати аналізу
    response_data = {k: serialize(v) for k, v in results.items()}
    
    # Додавання прогнозів загроз
    if ai_models_available:
        # Використання AI-моделей для прогнозування
        predictions = predict_threats(results['data'])
        response_data['predictions'] = predictions
    else:
        # Імітація прогнозів, якщо AI-моделі недоступні
        response_data['predictions'] = generate_mock_predictions()
    
    # Додавання рекомендацій та рішень
    response_data['recommendations'] = generate_recommendations(response_data)
    response_data['decisions'] = get_recent_decisions()
    
    return jsonify(response_data)

@app.route('/api/simulate-scenario', methods=['POST'])
def simulate_scenario_api():
    data = request.json
    location = data.get('location')
    threat_type = data.get('threat_type')
    intensity = data.get('intensity', 5)
    
    if ai_models_available:
        # Використання AI-моделей для моделювання сценарію
        result = simulate_scenario(location, threat_type, intensity)
    else:
        # Імітація результатів моделювання
        result = generate_mock_scenario_result(location, threat_type, intensity)
    
    return jsonify(result)

# Допоміжні функції для генерації імітаційних даних
def generate_mock_predictions():
    locations = ['Харків', 'Донецьк', 'Луганськ', 'Запоріжжя', 'Херсон', 'Миколаїв', 'Суми', 'Чернігів']
    threat_types = ['Артилерійський обстріл', 'Ракетний удар', 'Атака БПЛА', 'Мінометний обстріл', 'Снайперський вогонь']
    
    predictions = []
    for _ in range(8):
        location = random.choice(locations)
        threat_type = random.choice(threat_types)
        probability = random.uniform(10, 95)
        expected_casualties = int(probability / 20) if probability > 50 else 0
        
        predictions.append({
            'location': location,
            'threat_type': threat_type,
            'probability': probability,
            'expected_casualties': expected_casualties
        })
    
    return predictions

def generate_recommendations(data):
    recommendations = [
        {
            'title': 'Посилення оборонних позицій',
            'description': 'Рекомендується посилити оборонні позиції в районах з високим рівнем загрози.',
            'priority': random.randint(7, 10),
            'expected_effectiveness': random.randint(6, 9)
        },
        {
            'title': 'Евакуація цивільного населення',
            'description': 'Рекомендується провести евакуацію цивільного населення з районів можливих обстрілів.',
            'priority': random.randint(5, 9),
            'expected_effectiveness': random.randint(7, 10)
        },
        {
            'title': 'Розгортання медичних пунктів',
            'description': 'Рекомендується розгорнути додаткові медичні пункти для надання допомоги пораненим.',
            'priority': random.randint(6, 8),
            'expected_effectiveness': random.randint(7, 9)
        },
        {
            'title': 'Посилення розвідки',
            'description': 'Рекомендується посилити розвідувальні заходи для виявлення загроз.',
            'priority': random.randint(4, 8),
            'expected_effectiveness': random.randint(5, 8)
        },
        {
            'title': 'Ротація особового складу',
            'description': 'Рекомендується провести ротацію особового складу в районах з високою інтенсивністю бойових дій.',
            'priority': random.randint(3, 7),
            'expected_effectiveness': random.randint(5, 8)
        }
    ]
    
    return recommendations

def get_recent_decisions():
    decisions = [
        {
            'timestamp': (datetime.now() - timedelta(days=2)).isoformat(),
            'description': 'Посилення оборонних позицій в районі Харкова',
            'action_taken': 'Направлено додаткові інженерні підрозділи',
            'result': 'Зменшення втрат від артилерійських обстрілів',
            'effectiveness': 8
        },
        {
            'timestamp': (datetime.now() - timedelta(days=5)).isoformat(),
            'description': 'Евакуація цивільного населення з Херсона',
            'action_taken': 'Організовано евакуаційні коридори',
            'result': 'Евакуйовано 80% цивільного населення',
            'effectiveness': 9
        },
        {
            'timestamp': (datetime.now() - timedelta(days=7)).isoformat(),
            'description': 'Розгортання додаткових медичних пунктів',
            'action_taken': 'Створено 3 мобільні медичні бригади',
            'result': 'Покращено надання медичної допомоги пораненим',
            'effectiveness': 7
        },
        {
            'timestamp': (datetime.now() - timedelta(days=10)).isoformat(),
            'description': 'Посилення розвідки в районі Донецька',
            'action_taken': 'Залучено додаткові розвідувальні групи',
            'result': 'Виявлено 5 нових загроз',
            'effectiveness': 6
        },
        {
            'timestamp': (datetime.now() - timedelta(days=15)).isoformat(),
            'description': 'Ротація особового складу в районі Луганська',
            'action_taken': 'Проведено ротацію 2 батальйонів',
            'result': 'Підвищено боєздатність підрозділів',
            'effectiveness': 8
        }
    ]
    
    return decisions

def generate_mock_scenario_result(location, threat_type, intensity):
    # Конвертація типу загрози в читабельний формат
    threat_type_readable = {
        'artillery': 'Артилерійський обстріл',
        'rocket': 'Ракетний удар',
        'drone': 'Атака БПЛА',
        'mortar': 'Мінометний обстріл',
        'sniper': 'Снайперський вогонь'
    }.get(threat_type, threat_type)
    
    # Розрахунок рівня ризику на основі інтенсивності
    risk_level = min(10, intensity + random.randint(-1, 2))
    
    # Розрахунок очікуваних втрат
    expected_casualties = int((risk_level / 10) * intensity * random.uniform(0.5, 1.5))
    expected_wounded = int((risk_level / 10) * intensity * random.uniform(1.0, 3.0))
    
    # Генерація рекомендацій
    recommendations = []
    if risk_level >= 7:
        recommendations.append("Негайна евакуація особового складу з небезпечної зони")
        recommendations.append("Розгортання додаткових медичних пунктів")
    elif risk_level >= 4:
        recommendations.append("Посилення оборонних позицій")
        recommendations.append("Підготовка до можливої евакуації")
    else:
        recommendations.append("Підвищення рівня готовності")
        recommendations.append("Посилення розвідки")
    
    return {
        'location': location,
        'threat_type': threat_type_readable,
        'intensity': intensity,
        'risk_level': risk_level,
        'expected_casualties': expected_casualties,
        'expected_wounded': expected_wounded,
        'recommendations': ", ".join(recommendations)
    }

if __name__ == '__main__':
    app.run(debug=True)