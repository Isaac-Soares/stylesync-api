from flask import Flask
from pymongo import MongoClient

db = None

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    global db

    try:
        client = MongoClient(app.config['MONGO_URI'])
        db = client.get_default_database()

    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

    # Suas rotas antigas da API
    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    # --- ADICIONE ESTAS DUAS LINHAS ABAIXO ---
    # Suas novas rotas de telas HTML
    from .routes.frontend import frontend_bp
    app.register_blueprint(frontend_bp)

    return app