from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask.ext.cors import CORS
import logging

app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)
logging.basicConfig(level=logging.DEBUG)

# Create database connection object
db = MongoEngine(app)

# Security needs the Mail plugin configured for confirmations/resets
mail = Mail(app)

#cors = CORS(app, resources={r"/ajax/*": {"origins": "*"},r"/login": {"supports_credentials": True}})
cors = CORS(app)

from .home.views import home
from .static import global_static
from .auth import auth
from .ajax import ajax
app.register_blueprint(home)
app.register_blueprint(global_static,static_folder='static')
app.register_blueprint(auth)
app.register_blueprint(ajax)

