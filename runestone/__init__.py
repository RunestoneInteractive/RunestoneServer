from flask import Flask
from .home.views import home
from .static import global_static

app = Flask(__name__)
app.register_blueprint(home)
app.register_blueprint(global_static,static_folder='static')

