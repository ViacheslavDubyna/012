# Ініціалізація модуля дашборду для інформаційно-аналітичної системи Національної гвардії України

from flask import Flask, Blueprint

dashboard = Blueprint('dashboard', __name__, template_folder='templates', static_folder='static')

# Імпортуємо маршрути дашборду
from .routes import *