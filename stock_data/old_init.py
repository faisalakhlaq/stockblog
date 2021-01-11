from flask import Flask

from .old_config import Config


app = Flask(__name__)
app.config.from_object(Config)

from stock_data import routes

