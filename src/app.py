"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, Favorites, Favplanet, Favpeople
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Get, Post and Delete User
# Get all user
@app.route('/user', methods=['GET'])
def handle_hello():
    users = User.query.all()
    response_user = [user.serialize() for user in users]
    response_body = {
        "msg": "Users list"
    }

    return jsonify(response_user), 200
#Get a one single user information
@app.route('/user/<int:user_id>', methods=['GET'])
def select_user(user_id):
    # user = list(filter(lambda element: element['id'] == user_id, users))
    user = User.query.get(user_id)
    user = user.serialize()
    return jsonify(user), 200

# Get, Post and Delete People
# Get all People
@app.route('/people', methods=['GET'])
def handle_people():
    peoples = People.query.all()
    result_people = [people.serialize() for people in peoples]
    return jsonify(result_people), 200

# Get a one single people information
@app.route('/people/<int:people_id>', methods=['GET'])
def select_people(people_id):
    person = People.query.get(people_id)
    person = person.serialize()
    return jsonify(person), 200

# Add people
@app.route('/people', methods=['POST'])
def create_people():
    data = request.data
    data = json.loads(data)

    person = People(name = data['name'], mass = data['mass'])
    db.session.add(person)
    db.session.commit()
    response_body = {
        "msg": "Todo Ok! "
    }
    return jsonify(response_body), 200

# Delete People
@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):
    person_delete = People.query.get(people_id)
    db.session.delete(person_delete)
    db.session.commit()

    response_body = {
        "msg": "Borrado! "
    }
    return jsonify(response_body), 200

# Get, Post and Delete Planets
# Get all Planet
@app.route('/planet', methods=['GET'])
def handle_planet():
    planets = Planet.query.all()
    # result = []
    # for planet in planets:
    #     result.append(planet.serialize())
    result = [planet.serialize() for planet in planets]
    return jsonify(result), 200

# Get a one single planet information
@app.route('/planet/<int:planet_id>', methods=['GET'])
def select_planet(planet_id):
    planet = Planet.query.get(planet_id)
    planet = planet.serialize()
    return jsonify(planet), 200

# Add planet
@app.route('/planet', methods=['POST'])
def create_planet():  
    data = request.data
    data = json.loads(data)

    planet = Planet(name = data['name'], rotation_period = data['rotation_period'])
    db.session.add(planet)
    db.session.commit()
    response_body = {
        "msg": "Todo Ok! "
    }
    return jsonify(response_body), 200

# Delete planet
@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id): 
    planet_delete = Planet.query.get(planet_id)
    db.session.delete(planet_delete)
    db.session.commit()
    
    response_body = {
        "msg": "Borrado! "
    }
    return jsonify(response_body), 200    

# Get, post and delete Favorites
# Get all Favorite, table Favorite
@app.route('/favorite', methods=['GET'])
def handle_fav():
    # favorites = Favorites.query.filter_by(id == user_id)
    favorites = Favorites.query.all()
    fav = [favorite.serialize() for favorite in favorites]

    return jsonify(fav), 200

#  Get all the favorites that belong to the current user, table Favorite
@app.route('/favorite/<int:id>', methods=['GET'])
def select_fav(id):
    fav = Favorites.query.filter_by(user_id = id).all()
    favorite_user = [favorite.serialize() for favorite in fav]
    print(fav)
    return jsonify(favorite_user), 200

# Add Add a new planet or people at table Favorite
@app.route('/favorite', methods=['POST'])
def new_fav():  
    data = request.data
    data = json.loads(data)

    fav = Favorites(user_id = data['user_id'], planet_id = data['planet_id'], people_id = data['people_id'])
    db.session.add(fav)
    db.session.commit()
    response_body = {
        "msg": "Todo Ok! "
    }
    return jsonify(response_body), 200

#  Add a new favorite planet to the current user with the planet id = planet_id (table Favplanet)
@app.route('/favorite/planet/<int:id>', methods=['POST'])
def new_fav_planet(id):
    data = request.data
    data = json.loads(data)

    fav_planet = Favplanet(user_id_plan = data['user_id_plan'], planet_fav = id)
    db.session.add(fav_planet)
    db.session.commit()

    response_body = {
        "msg": "Todo Ok! "
    }
    return jsonify(response_body), 200

# Add a new favorite people to the current user with the people id = people_id. (table Favpeople)
@app.route('/favorite/people/<int:id>', methods=['POST'])
def new_fav_people(id):
    data = request.data
    data = json.loads(data)

    fav_people = Favpeople(user_id_people = data['user_id_people'], people_fav = id)
    db.session.add(fav_people)
    db.session.commit()

    response_body = {
        "msg": "Todo Ok! "
    }
    return jsonify(response_body), 200

# Delete favorite planet with the id = planet_id
@app.route('/favorite/planet/<int:id>', methods=['DELETE'])
def delete_fav_planet(id): 
    planet_delete = Favplanet.query.filter_by(user_id_plan = 1, planet_fav = id).first()
    
    db.session.delete(planet_delete)
    db.session.commit()
    response_body = {
        "msg": "Borrado! "
    }
    return jsonify(response_body), 200

# Delete favorite people with the id = people_id
@app.route('/favorite/people/<int:id>', methods=['DELETE'])
def delete_fav_people(id): 
    people_delete = Favpeople.query.filter_by(user_id_people = 1, people_fav = id).first()
    
    db.session.delete(people_delete)
    db.session.commit()
    response_body = {
        "msg": "Borrado! "
    }
    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
