__author__ = 'bmiller'
from flask import Flask, Blueprint, render_template, jsonify, request

from flask.ext.security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required

from runestone import db, app
from runestone.model import *
from flask.ext.cors import cross_origin

ajax = Blueprint('ajax', __name__,
          template_folder='templates',static_folder='static')


@ajax.route('/ajax/page')
@login_required
@cross_origin(supports_credentials=True)
def test():
    return jsonify({'foo':'bar'})


