from urllib import response
from flask import Blueprint, render_template, request, jsonify
from dc_app.helpers import token_required
from dc_app.models import db, User, Hero, hero_schema, heroes_schema, Villain, villain_schema, villains_schema
from dc_app.forms import UserSignUpForm

api = Blueprint('api', __name__,
                template_folder='api_templates', url_prefix='/api')


@api.route('/heroes', methods=['POST'])
@token_required
def create_hero(current_user_token):
    image = request.json['image']
    alias = request.json['alias']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    origin = request.json['origin']
    location = request.json['location']
    power = request.json['power']
    bio = request.json['bio']
    user_token = current_user_token.token
    print(user_token)
    hero = Hero(alias, user_token, first_name, last_name,
                origin, location, power, bio, image)

    db.session.add(hero)
    db.session.commit()

    response = hero_schema.dump(hero)

    return jsonify(response)


@api.route('/villains', methods=['POST'])
@token_required
def create_villain(current_user_token):
    image = request.json['image']
    alias = request.json['alias']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    origin = request.json['origin']
    location = request.json['location']
    power = request.json['power']
    bio = request.json['bio']
    user_token = current_user_token.token

    villain = Villain(alias, user_token, first_name, last_name,
                      origin, location, power, bio, image)

    db.session.add(villain)
    db.session.commit()

    response = villain_schema.dump(villain)

    return jsonify(response)


@api.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.order_by(Hero.alias).all()
    response = heroes_schema.dump(heroes)

    return jsonify(response)


@api.route('/villains', methods=['GET'])
def get_villains():
    villains = Villain.query.order_by(Villain.alias).all()
    response = villains_schema.dump(villains)

    return jsonify(response)


@api.route('/heroes/<id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    response = hero_schema.dump(hero)
    return jsonify(response)


@api.route('/villains/<id>', methods=['GET'])
def get_villain(id):
    villain = Villain.query.get(id)
    response = villain_schema.dump(villain)
    return jsonify(response)

# Render Templates


@api.route('/hero', methods=['GET'])
def hero_home():
    h = Hero.query.all()
    return render_template('hero.html', hero=h)


@api.route('/villain')
def villain_home():
    v = Villain.query.all()
    return render_template('villain.html', villain=v)


@api.route('/hero/<id>', methods=['GET'])
def get_hero_id(id):
    hero = Hero.query.get(id)
    return render_template('hero_id.html', hero=hero)


@api.route('/villain/<id>', methods=['GET'])
def get_villain_id(id):
    villain = Villain.query.get(id)
    return render_template('villain_id.html', villain=villain)


# User API CRUD

@api.route('/user/<id>', methods=['POST', 'PUT'])
@token_required
def update_user(current_user_token, id):
    user = User.query.get(id)
    form = UserSignUpForm()
