import helpers
import re
import random
from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from models import db
from models import User, Pokemon, UserPokemon

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Change this to a random value
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokehang.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


app = create_app()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Password validation
        if not re.match(r'^(?=.*[A-Za-z]{4})(?=.*\d)[A-Za-z\d]{5,}$', password):
            flash('Password must contain at least 4 letters and 1 number.', 'danger')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        print(existing_user)
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('You have successfully registered! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.username  # Set the user_name attribute in the session
            flash('You have successfully logged in!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        return render_template('profile.html', user=user)
    else:
        flash('You need to log in first.', 'error')
        return redirect(url_for('login'))

@app.route('/game')
def game():
    all_pokemon = Pokemon.query.all()
    rndm_pokemon = random.choice(all_pokemon)
    print(rndm_pokemon.sprite_url)
    return render_template('game.html', rndm_pokemon=rndm_pokemon)

if __name__ == '__main__':
    app.run(debug=True)