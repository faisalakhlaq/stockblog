from stock_data import create_app
from stock_data.config import Config
from flask_wtf.csrf import CSRFProtect

app = create_app(Config)
csrf = CSRFProtect()
csrf.init_app(app)

if __name__ == '__main__':
    app.run()
