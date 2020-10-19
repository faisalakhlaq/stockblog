import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY')
    COINMARKET_API_KEY = os.environ.get('COINMARKET_API_KEY')
