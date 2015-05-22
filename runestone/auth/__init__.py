from flask import Flask, Blueprint, render_template

from flask.ext.security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required  

auth = Blueprint('auth', __name__,
          template_folder='templates',static_folder='static')
    
from runestone import db, app
from runestone.model import *

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)

# Create custom registration form here then add it on the constructor
# or maybe set it later with security.state.register_form
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
    user_datastore.create_user(email='matt@nobien.net', password='password')



# Views
@auth.route('/authtest')
@login_required
def home():
    return render_template('index.html')

