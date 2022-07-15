from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

import secrets
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def loaduser(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    image = db.Column(db.String, nullable = True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String)
    faction = db.Column(db.String(150), nullable = False)
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, unique = True)
    date_create = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    hero = db.relationship('Hero', backref = 'owner', lazy = True)
    villain = db.relationship('Villain', backref = 'owner', lazy = True)

    def __init__(self, email, faction, image = '', first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.faction = faction
        self.image = image
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify


    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f"User {self.email} has been added to the database"

class Hero(db.Model):
    id = db.Column(db.String, primary_key = True)
    image = db.Column(db.String, nullable = True)
    alias = db.Column(db.String(150))
    first_name = db.Column(db.String(150), nullable = True)
    last_name = db.Column(db.String(150), nullable = True)
    origin = db.Column(db.String(200), nullable = True)
    location = db.Column(db.String(200), nullable = True)
    power = db.Column(db.String(200))
    bio = db.Column(db.String(600), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, alias, user_token, first_name = '', last_name = '', origin = '', location = '', power = '', bio = '', image = '', id = ''):
        self.id = self.set_id()
        self.alias = alias
        self.first_name = first_name
        self.last_name = last_name
        self.origin = origin
        self.location = location
        self.power = power
        self.bio = bio
        self.image = image
        self.user_token = user_token

    def __repr__(self):
        return f"The following Hero has been added {self.name}"
        
    def set_id(self):
        return secrets.token_urlsafe()

class Villain(db.Model):
    id = db.Column(db.String, primary_key = True)
    image = db.Column(db.String, nullable = True)
    alias = db.Column(db.String(150))
    first_name = db.Column(db.String(150), nullable = True)
    last_name = db.Column(db.String(150), nullable = True)
    origin = db.Column(db.String(200), nullable = True)
    location = db.Column(db.String(200), nullable = True)
    power = db.Column(db.String(200))
    bio = db.Column(db.String(600), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, alias, user_token, first_name = '', last_name = '', origin = '', location = '', power = '', bio = '', image = '', id = ''):
        self.id = self.set_id()
        self.alias = alias
        self.first_name = first_name
        self.last_name = last_name
        self.origin = origin
        self.location = location
        self.power = power
        self.bio = bio
        self.image = image
        self.user_token = user_token

    def __repr__(self):
        return f"The following Villain has been added {self.name}"
        
    def set_id(self):
        return secrets.token_urlsafe()


class HeroSchema(ma.Schema):
		    class Meta:
		        fields = ["id", "alias", "first_name", "last_name", "origin", "location", "power", "bio", "image"]

hero_schema = HeroSchema()
heroes_schema = HeroSchema(many=True) 

class VillainSchema(ma.Schema):
		    class Meta:
		        fields = ["id", "alias", "first_name", "last_name", "origin", "location", "power", "bio", "image"]

villain_schema = VillainSchema()
villains_schema = VillainSchema(many=True) 