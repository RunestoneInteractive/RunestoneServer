from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devdb.db'

# Create database connection object
db = SQLAlchemy(app)

from .home.views import home
from .static import global_static
from .auth import auth
app.register_blueprint(home)
app.register_blueprint(global_static,static_folder='static')
app.register_blueprint(auth)
