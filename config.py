import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'splash.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Set to False for better performance

    # Mail settings
    MAIL_SERVER = os.getenv('MAIL_SERVER', '')
    MAIL_SENDER = os.getenv('MAIL_SENDER', '')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 465))  # Convert to integer
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'False').lower() == 'true'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'True').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')

    # Admin and uploads
    ADMIN = os.getenv('ADMIN', '')
    UPLOAD_EXTENSIONS = [".jpg", ".png"]
    UPLOAD_PATH = "app/static/uploads"
