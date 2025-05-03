#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Маршрути дашборду для інформаційно-аналітичної системи НГУ

Цей модуль містить всі маршрути для веб-інтерфейсу системи.
"""

from flask import render_template, request, redirect, url_for, flash, current_app
from ias_NGU.dashboard import dashboard_bp


@dashboard_bp.route('/')
def index():
    """Головна сторінка дашборду"""
    return render_template('index.html', title='Головна - НГУ ІАС')


@dashboard_bp.route('/statistics')
def statistics():
    """Сторінка статистики"""
    # Тут буде логіка отримання статистичних даних для відображення
    return render_template('statistics.html', title='Статистика - НГУ ІАС')


@dashboard_bp.route('/analytics')
def analytics():
    """Сторінка аналітики"""
    # Тут буде логіка отримання аналітичних даних для відображення
    return render_template('analytics.html', title='Аналітика - НГУ ІАС')


@dashboard_bp.route('/predictions')
def predictions():
    """Сторінка прогнозів"""
    # Тут буде логіка отримання прогнозів для відображення
    return render_template('predictions.html', title='Прогнози - НГУ ІАС')


@dashboard_bp.route('/incidents')
def incidents():
    """Сторінка інцидентів"""
    # Тут буде логіка отримання списку інцидентів для відображення
    return render_template('incidents.html', title='Інциденти - НГУ ІАС')


@dashboard_bp.route('/incidents/<int:incident_id>')
def incident_details(incident_id):
    """Сторінка деталей інциденту"""
    # Тут буде логіка отримання деталей інциденту для відображення
    return render_template('incident_details.html', title='Деталі інциденту - НГУ ІАС', incident_id=incident_id)


@dashboard_bp.route('/settings')
def settings():
    """Сторінка налаштувань"""
    return render_template('settings.html', title='Налаштування - НГУ ІАС')