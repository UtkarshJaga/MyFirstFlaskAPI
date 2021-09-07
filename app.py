import os
import re
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# Flask-JWT (Json web Token)

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ivinoklytolycj:938350ffef100080b272a7e69bab5d3ff150c6da7e6df4502a379f0b3dd94dcd@ec2-35-153-114-74.compute-1.amazonaws.com:5432/d68ucfd5bpa23u'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'utkarsh'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)