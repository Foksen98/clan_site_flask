from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from config.config import DevConfig, ProdConfig


app = Flask(__name__)
app.config.from_object(DevConfig)

db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.session_protection = "strong"
