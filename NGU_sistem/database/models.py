#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Моделі бази даних для інформаційно-аналітичної системи ДПСУ

Цей модуль містить визначення моделей даних для роботи з базою даних.
"""

from datetime import datetime
from ias_DPSU.database import db


class Incident(db.Model):
    """Модель для інцидентів на кордоні"""
    __tablename__ = 'incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(255), nullable=False)
    coordinates = db.Column(db.String(100), nullable=True)  # формат: "lat,lng"
    severity = db.Column(db.String(50), nullable=False)  # низька, середня, висока
    status = db.Column(db.String(50), nullable=False)  # активний, вирішений, архівований
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Incident {self.id}: {self.title}>"


class BorderCrossing(db.Model):
    """Модель для перетинів кордону"""
    __tablename__ = 'border_crossings'
    
    id = db.Column(db.Integer, primary_key=True)
    checkpoint = db.Column(db.String(255), nullable=False)
    direction = db.Column(db.String(50), nullable=False)  # в'їзд, виїзд
    vehicle_type = db.Column(db.String(50), nullable=True)  # легковий, вантажний, пішохід
    count = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<BorderCrossing {self.id}: {self.checkpoint} - {self.date}>"


class User(db.Model):
    """Модель для користувачів системи"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # адміністратор, аналітик, оператор
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f"<User {self.id}: {self.username}>"


class Report(db.Model):
    """Модель для звітів та аналітичних документів"""
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    report_type = db.Column(db.String(50), nullable=False)  # щоденний, тижневий, місячний, спеціальний
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Зв'язок з користувачем, який створив звіт
    user = db.relationship('User', backref=db.backref('reports', lazy=True))
    
    def __repr__(self):
        return f"<Report {self.id}: {self.title}>"