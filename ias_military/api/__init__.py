# Ініціалізація API модуля для інформаційно-аналітичної системи Національної гвардії України

from flask import Blueprint

app = Blueprint('api', __name__)

# Імпортуємо маршрути API
from .routes import *