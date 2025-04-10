# Скрипт для заповнення бази даних тестовими даними

import datetime
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, OperationalSituation, NGUUnit, Resource, ResourceAllocation, Incident, Decision, Prediction

def seed_database(db_url):
    """Заповнення бази даних тестовими даними"""
    # Підключення до бази даних
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Створення підрозділів НГУ
    units = [
        NGUUnit(
            name=f"Військова частина {3000+i}",
            unit_type=random.choice(["Оперативного призначення", "Спеціального призначення", "Охорони ОВВ", "Конвойний", "Охорони дипломатичних представництв"]),
            location=random.choice(["Київ", "Харків", "Львів", "Одеса", "Дніпро", "Запоріжжя", "Миколаїв", "Вінниця"]),
            region=random.choice(["Північ", "Південь", "Схід", "Захід", "Центр", "Київ"]),
            personnel_count=random.randint(100, 1000),
            commander=f"Полковник Іванов І.І. {i}",
            readiness_level=random.randint(1, 5),
            last_updated=datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))
        ) for i in range(10)
    ]
    session.add_all(units)
    session.commit()
    
    # Створення оперативних ситуацій
    situations = []
    for i in range(30):
        date = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 60))
        situation = OperationalSituation(
            timestamp=date,
            location=random.choice(["Київ", "Харків", "Львів", "Одеса", "Дніпро", "Запоріжжя", "Миколаїв", "Вінниця"]),
            region=random.choice(["Північ", "Південь", "Схід", "Захід", "Центр", "Київ"]),
            status=random.choice(["Штатна", "Напружена", "Критична", "Надзвичайна"]),
            threat_level=random.randint(1, 5),
            description=f"Оперативна ситуація #{i+1}",
            unit_id=random.choice(units).id
        )
        situations.append(situation)
    session.add_all(situations)
    session.commit()
    
    # Створення ресурсів
    resources = []
    resource_types = ["Особовий склад", "Техніка", "Озброєння", "Боєприпаси", "Спорядження"]
    resource_subtypes = {
        "Особовий склад": ["Офіцери", "Сержанти", "Солдати"],
        "Техніка": ["Автомобілі", "Бронетехніка", "Спецтехніка"],
        "Озброєння": ["Стрілецька зброя", "Гранатомети", "Важке озброєння"],
        "Боєприпаси": ["Набої", "Гранати", "Міни"],
        "Спорядження": ["Бронежилети", "Шоломи", "Спецзасоби"]
    }
    
    for unit in units:
        for _ in range(random.randint(5, 15)):
            resource_type = random.choice(resource_types)
            resource = Resource(
                type=resource_type,
                subtype=random.choice(resource_subtypes[resource_type]),
                quantity=random.randint(10, 1000),
                status=random.choice(["Доступний", "Розгорнутий", "На обслуговуванні", "Резерв"]),
                location=unit.location,
                unit_id=unit.id,
                last_updated=datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))
            )
            resources.append(resource)
    session.add_all(resources)
    session.commit()
    
    # Створення інцидентів
    incidents = []
    incident_types = ["Порушення громадського порядку", "Терористична загроза", "Диверсія", "Масові заворушення", "Блокування об'єктів"]
    
    for situation in situations:
        for _ in range(random.randint(0, 5)):
            incident = Incident(
                situation_id=situation.id,
                type=random.choice(incident_types),
                subtype="Підтип інциденту",
                description=f"Опис інциденту для ситуації {situation.id}",
                location=situation.location,
                coordinates=f"{random.uniform(44.0, 52.0):.6f}, {random.uniform(22.0, 40.0):.6f}",
                timestamp=situation.timestamp + datetime.timedelta(hours=random.randint(0, 24)),
                severity=random.randint(1, 5),
                status=random.choice(["Активний", "Вирішений", "В процесі"]),
                casualties=random.randint(0, 10),
                property_damage=random.choice([True, False])
            )
            incidents.append(incident)
    session.add_all(incidents)
    session.commit()
    
    # Створення розподілу ресурсів
    allocations = []
    for situation in situations:
        for _ in range(random.randint(1, 5)):
            resource = random.choice(resources)
            allocation = ResourceAllocation(
                resource_id=resource.id,
                situation_id=situation.id,
                quantity_allocated=random.randint(1, resource.quantity),
                allocation_time=situation.timestamp + datetime.timedelta(hours=random.randint(1, 12)),
                allocation_status=random.choice(["Заплановано", "В процесі", "Завершено"]),
                priority=random.randint(1, 5),
                notes=f"Розподіл ресурсів для ситуації {situation.id}"
            )
            allocations.append(allocation)
    session.add_all(allocations)
    session.commit()
    
    # Створення рішень
    decisions = []
    decision_types = ["Розгортання сил", "Евакуація", "Блокування території", "Патрулювання", "Охорона об'єкту"]
    
    for situation in situations:
        for _ in range(random.randint(1, 3)):
            decision_time = situation.timestamp + datetime.timedelta(hours=random.randint(1, 6))
            implementation_time = decision_time + datetime.timedelta(hours=random.randint(1, 12))
            decision = Decision(
                situation_id=situation.id,
                decision_type=random.choice(decision_types),
                description=f"Рішення для ситуації {situation.id}",
                decision_maker=f"Командир підрозділу {situation.unit_id}",
                decision_time=decision_time,
                implementation_time=implementation_time,
                status=random.choice(["Прийнято", "Виконується", "Виконано", "Скасовано"]),
                effectiveness_score=random.randint(1, 10),
                notes=f"Примітки до рішення для ситуації {situation.id}"
            )
            decisions.append(decision)
    session.add_all(decisions)
    session.commit()
    
    # Створення прогнозів
    predictions = []
    prediction_types = ["Загроза", "Ресурси", "Інциденти"]
    
    for _ in range(50):
        prediction_type = random.choice(prediction_types)
        prediction_value = random.uniform(1, 10)
        actual_outcome = prediction_value * random.uniform(0.7, 1.3)  # Симуляція фактичного результату
        accuracy = 1 - abs(prediction_value - actual_outcome) / prediction_value  # Розрахунок точності
        
        prediction = Prediction(
            timestamp=datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 60)),
            prediction_type=prediction_type,
            location=random.choice(["Київ", "Харків", "Львів", "Одеса", "Дніпро", "Запоріжжя", "Миколаїв", "Вінниця"]),
            region=random.choice(["Північ", "Південь", "Схід", "Захід", "Центр", "Київ"]),
            prediction_value=prediction_value,
            confidence=random.uniform(0.6, 0.95),
            description=f"Прогноз {prediction_type.lower()}",
            actual_outcome=actual_outcome,
            accuracy=accuracy
        )
        
        # Додаткові поля в залежності від типу прогнозу
        if prediction_type == "Загроза":
            prediction.threat_type = random.choice(["Високий рівень загрози", "Низький рівень загрози"])
        elif prediction_type == "Ресурси":
            prediction.resource_type = random.choice(["Особовий склад", "Техніка", "Озброєння", "Боєприпаси", "Спорядження"])
        elif prediction_type == "Інциденти":
            prediction.incident_type = random.choice(["Порушення громадського порядку", "Терористична загроза", "Диверсія", "Масові заворушення", "Блокування об'єктів"])
        
        predictions.append(prediction)
    session.add_all(predictions)
    session.commit()
    
    print(f"Додано {len(units)} підрозділів НГУ")
    print(f"Додано {len(situations)} оперативних ситуацій")
    print(f"Додано {len(resources)} ресурсів")
    print(f"Додано {len(incidents)} інцидентів")
    print(f"Додано {len(allocations)} розподілів ресурсів")
    print(f"Додано {len(decisions)} рішень")
    print(f"Додано {len(predictions)} прогнозів")
    
    return True