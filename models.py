from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ChatGPT helped here
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    end_url = db.Column(db.String(100), nullable=False)
    sprite_url = db.Column(db.String(100), nullable=False)

class UserPokemon(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), primary_key=True)