# Ініціалізація API модуля для інформаційно-аналітичної системи Національної гвардії України

from flask import Flask

app = Flask(__name__)

# Імпортуємо маршрути API
from .routes import *