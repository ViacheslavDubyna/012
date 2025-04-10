# Моделі бази даних для інформаційно-аналітичної системи Національної гвардії України

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
import datetime

Base = declarative_base()

# Перелік регіонів відповідальності НГУ
class RegionEnum(enum.Enum):
    ПІВНІЧ = "Північ"
    ПІВДЕНЬ = "Південь"
    СХІД = "Схід"
    ЗАХІД = "Захід"
    ЦЕНТР = "Центр"
    КИЇВ = "Київ"

# Перелік типів підрозділів НГУ
class UnitTypeEnum(enum.Enum):
    ОПЕРАТИВНОГО_ПРИЗНАЧЕННЯ = "Оперативного призначення"
    СПЕЦІАЛЬНОГО_ПРИЗНАЧЕННЯ = "Спеціального призначення"
    ОХОРОНИ_ОВВ = "Охорони ОВВ"
    КОНВОЙНИЙ = "Конвойний"
    ОХОРОНИ_ДИПЛОМАТИЧНИХ_ПРЕДСТАВНИЦТВ = "Охорони дипломатичних представництв"

# Перелік статусів оперативної обстановки
class StatusEnum(enum.Enum):
    ШТАТНА = "Штатна"
    НАПРУЖЕНА = "Напружена"
    КРИТИЧНА = "Критична"
    НАДЗВИЧАЙНА = "Надзвичайна"

# Модель оперативної обстановки
class OperationalSituation(Base):
    __tablename__ = 'operational_situation'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.now)
    location = Column(String(50), nullable=False)
    region = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    threat_level = Column(Integer, nullable=False)  # Від 1 до 5
    description = Column(Text)
    unit_id = Column(Integer, ForeignKey('ngu_units.id'))
    
    # Зв'язки
    incidents = relationship("Incident", back_populates="situation")
    unit = relationship("NGUUnit", back_populates="situations")
    resource_allocations = relationship("ResourceAllocation", back_populates="situation")
    decisions = relationship("Decision", back_populates="situation")

# Модель підрозділів НГУ
class NGUUnit(Base):
    __tablename__ = 'ngu_units'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    unit_type = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    region = Column(String(50), nullable=False)
    personnel_count = Column(Integer)
    commander = Column(String(100))
    readiness_level = Column(Integer)  # Від 1 до 5
    last_updated = Column(DateTime, default=datetime.datetime.now)
    
    # Зв'язки
    situations = relationship("OperationalSituation", back_populates="unit")
    resources = relationship("Resource", back_populates="unit")

# Модель ресурсів
class Resource(Base):
    __tablename__ = 'resources'
    
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)  # Особовий склад, Техніка, Озброєння, Боєприпаси, Спорядження
    subtype = Column(String(100))  # Конкретний тип ресурсу
    quantity = Column(Integer)
    status = Column(String(50))  # Доступний, Розгорнутий, На обслуговуванні, Резерв
    location = Column(String(100))
    unit_id = Column(Integer, ForeignKey('ngu_units.id'))
    last_updated = Column(DateTime, default=datetime.datetime.now)
    
    # Зв'язки
    unit = relationship("NGUUnit", back_populates="resources")
    allocations = relationship("ResourceAllocation", back_populates="resource")

# Модель розподілу ресурсів
class ResourceAllocation(Base):
    __tablename__ = 'resource_allocations'
    
    id = Column(Integer, primary_key=True)
    resource_id = Column(Integer, ForeignKey('resources.id'))
    situation_id = Column(Integer, ForeignKey('operational_situation.id'))
    quantity_allocated = Column(Integer, nullable=False)
    allocation_time = Column(DateTime, default=datetime.datetime.now)
    allocation_status = Column(String(50))  # Заплановано, В процесі, Завершено
    priority = Column(Integer)  # Від 1 до 5
    notes = Column(Text)
    
    # Зв'язки
    resource = relationship("Resource", back_populates="allocations")
    situation = relationship("OperationalSituation", back_populates="resource_allocations")

# Модель інцидентів
class Incident(Base):
    __tablename__ = 'incidents'
    
    id = Column(Integer, primary_key=True)
    situation_id = Column(Integer, ForeignKey('operational_situation.id'))
    type = Column(String(50), nullable=False)  # Порушення громадського порядку, Терористична загроза, Диверсія, тощо
    subtype = Column(String(100))
    description = Column(Text)
    location = Column(String(100))
    coordinates = Column(String(100))  # Географічні координати
    timestamp = Column(DateTime, default=datetime.datetime.now)
    severity = Column(Integer)  # Від 1 до 5
    status = Column(String(50))  # Активний, Вирішений, В процесі
    casualties = Column(Integer, default=0)
    property_damage = Column(Boolean, default=False)
    
    # Зв'язки
    situation = relationship("OperationalSituation", back_populates="incidents")

# Модель рішень
class Decision(Base):
    __tablename__ = 'decisions'
    
    id = Column(Integer, primary_key=True)
    situation_id = Column(Integer, ForeignKey('operational_situation.id'))
    decision_type = Column(String(50), nullable=False)  # Розгортання сил, Евакуація, Блокування території, тощо
    description = Column(Text)
    decision_maker = Column(String(100))
    decision_time = Column(DateTime, default=datetime.datetime.now)
    implementation_time = Column(DateTime)
    status = Column(String(50))  # Прийнято, Виконується, Виконано, Скасовано
    effectiveness_score = Column(Integer)  # Від 1 до 10
    notes = Column(Text)
    
    # Зв'язки
    situation = relationship("OperationalSituation", back_populates="decisions")

# Модель прогнозів
class Prediction(Base):
    __tablename__ = 'predictions'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    prediction_type = Column(String(50), nullable=False)  # Загроза, Ресурси, Інциденти
    location = Column(String(100))
    region = Column(String(50))
    prediction_value = Column(Float)
    confidence = Column(Float)  # Від 0 до 1
    description = Column(Text)
    actual_outcome = Column(Float)
    accuracy = Column(Float)  # Розрахована після порівняння з фактичним результатом
    
    # Додаткові поля для різних типів прогнозів
    threat_type = Column(String(50))
    resource_type = Column(String(50))
    incident_type = Column(String(50))