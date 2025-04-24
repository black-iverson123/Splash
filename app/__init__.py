from flask import Flask, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from flask_moment import Moment
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'  # Update to match your auth Blueprint
login.session_protection = 'strong'
mail = Mail()
bootstrap = Bootstrap()
socketio = SocketIO(cors_allowed_origins="*")
moment = Moment()
CMC_API_KEY = os.getenv('API_KEY')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    socketio.init_app(app)
    moment.init_app(app)

    # Register Blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Redirect root URL to auth.index
    @app.route('/')
    def root():
        return redirect(url_for('auth.index'))

    return app