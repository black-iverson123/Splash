"""APP Environment handler"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """This class retrieves set environment variables and instatiates them"""
    SECRET_KEY = os.getenv('SECRET_KEY')  
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'splash.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') 
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 465))
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'True').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_SENDER = os.getenv('MAIL_SENDER', MAIL_USERNAME)
    API_KEY = os.getenv('API_KEY')

