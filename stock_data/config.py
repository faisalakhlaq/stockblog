import os


class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('HEIGHT_COLLECTOR_DATABASE_URI')
    # SQLALCHEMY_ECHO: When set to 'True', Flask-SQLAlchemy will log all database
    # activity to Python's stderr for debugging purposes.
    SQLALCHEMY_ECHO = False
    #  To suppress the warning "this option takes a lot of system resources" set
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY')

    # Flask-User settings
    # Shown email templates and page footers
    USER_APP_NAME = "Interactive Dict & Height Collector"
    # Configure email setting
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
