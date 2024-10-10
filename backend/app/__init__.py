import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Importar CORS
from .routes import init_routes
from .models import db

def create_app():
    app = Flask(__name__)
    
    # Configuración de la base de datos usando DATABASE_URL
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///links.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar CORS
    CORS(app)

    # Inicializar la base de datos
    db.init_app(app)

    with app.app_context():
        db.create_all()  # Crear las tablas si no existen

    # Importar y registrar las rutas
    init_routes(app)

    return app
