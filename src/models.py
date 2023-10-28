from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    rotation_period = db.Column(db.Integer, unique=False, nullable=True)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    mass = db.Column(db.Integer, unique=False, nullable=True)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "mass": self.mass,
            # do not serialize the password, its a security breach
        }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship(Planet)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    people = db.relationship(People)

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id
            # do not serialize the password, its a security breach
        }

class Favplanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id_plan = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    planet_fav = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship(Planet)

    def __repr__(self):
        return '<Planet Favortite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id_plat": self.user_id_plan,
            "planet_fav": self.planet_fav
        }

class Favpeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id_people = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    people_fav = db.Column(db.Integer, db.ForeignKey('people.id'))
    people = db.relationship(People)

    def __repr__(self):
        return '<People Favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id_peo": self.user_id_people,
            "people_fav": self.people_fav
        }
