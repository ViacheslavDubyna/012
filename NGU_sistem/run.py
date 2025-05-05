from flask import Flask
from dashboard.routes import dashboard_bp
from api.routes import api_bp
from config.config import Config
import os

app = Flask(__name__, 
           static_folder='static',
           static_url_path='/static')
app.config.from_object(Config)

# Реєстрація blueprints
app.register_blueprint(dashboard_bp, url_prefix='/')
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100)