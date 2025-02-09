import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'Darkside' or os.getenv('SECRET_KEY')  #create your secret key 
    # Specify your MySQL database name at the end of the connection string
    #SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') #set-up your database url
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'splash.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = '' or os.getenv('MAIL_SERVER')  #smtp.mailserver  
    MAIL_SENDER = '' or os.getenv('MAIL_SENDER') #mail sender     MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = '' or os.getenv('MAIL_USERNAME') #mail of choice username
    MAIL_PASSWORD = '' or os.getenv('MAIL_PASSWORD')#mail of choice password or app password
    ADMIN = '' or os.getenv('ADMIN')
    UPLOAD_EXTENSIONS = [".jpg", ".png"]
    UPLOAD_PATH = "app/static/uploads"
