import os


class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY')
    COINMARKET_API_KEY = os.environ.get('COINMARKET_API_KEY')

    DATABASE_URL = os.environ.get('HEROKU_STOCK_DB_URI')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    # SQLALCHEMY_ECHO: When set to 'True', Flask-SQLAlchemy will log all database
    # activity to Python's stderr for debugging purposes.
    SQLALCHEMY_ECHO = False
    #  To suppress the warning "this option takes a lot of system resources" set
    SQLALCHEMY_TRACK_MODIFICATIONS = False
