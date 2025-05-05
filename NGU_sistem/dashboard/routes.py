from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard_bp.route('/')
def index():
    return render_template('index.html', title='Головна | НГУ ІАС')

@dashboard_bp.route('/statistics')
def statistics():
    return render_template('statistics.html')

@dashboard_bp.route('/analytics')
def analytics():
    return render_template('analytics.html')

@dashboard_bp.route('/predictions')
def predictions():
    return render_template('predictions.html')

@dashboard_bp.route('/incidents')
def incidents():
    return render_template('incidents.html')