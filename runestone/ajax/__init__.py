__author__ = 'bmiller'
from flask import Flask, Blueprint, render_template, jsonify, request

from flask.ext.security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required

from runestone import db, app
from runestone.model import *
from flask.ext.cors import cross_origin
from flask_restful import Api, Resource

ajax = Blueprint('ajax', __name__,
          template_folder='templates',static_folder='static')

api = Api(app)

class HelloWorld(Resource):
    @cross_origin(supports_credentials=True)
    @login_required
    def get(self):
        return jsonify({'hello': 'world'})

api.add_resource(HelloWorld, '/ajax/page')


# @ajax.route('/ajax/page')
# @login_required
# @cross_origin(supports_credentials=True)
# def test():
#     return jsonify({'foo':'bar'})


