import os


class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URL = os.environ.get('HEROKU_STOCK_DB_URI')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    # SQLALCHEMY_ECHO: When set to 'True', Flask-SQLAlchemy will log all database
    # activity to Python's stderr for debugging purposes.
    SQLALCHEMY_ECHO = False
    #  To suppress the warning "this option takes a lot of system resources" set
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # TODO remove below two and device an appropriate method for image upload
    #  folder and extensions
    IMAGE_FOLDER = 'static/images'
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY')

    # Flask-User settings
    USER_APP_NAME = "Flask Basic App"  # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False  # Disable email authentication
    USER_ENABLE_USERNAME = True  # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = True  # Simplify register form
    # Configure email setting
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
