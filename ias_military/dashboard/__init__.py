# Ініціалізація модуля дашборду для інформаційно-аналітичної системи Національної гвардії України

from flask import Flask, Blueprint

dashboard = Blueprint('dashboard', __name__, template_folder='templates', static_folder='static')

# Імпортуємо маршрути дашборду
from .routes import *
# Імпортуємо маршрути для управління підрозділами
from .routes_unit import *
# Імпортуємо маршрути для управління інцидентами
from .routes_incident import *
# Імпортуємо маршрути для інструментів прогнозування та управління ресурсами
from .routes_prediction import *
# Імпортуємо маршрути для підтримки прийняття рішень та налаштувань
from .routes_decision import *
# Імпортуємо маршрути для вдосконаленого дашборду
from .improved_dashboard_routes import improved_dashboard, register_dashapp