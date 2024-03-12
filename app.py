import helpers
import string
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

@app.route('/game', methods=['GET', 'POST'])
def game():

    if 'rndm_pokemon_id' not in session or request.method == 'GET':
        reset_game()
        all_pokemon = Pokemon.query.all()
        rndm_pokemon = random.choice(all_pokemon)
        session['rndm_pokemon_id'] = rndm_pokemon.id
        session['letters'] = list(string.ascii_uppercase)
        session['guessed_chars'] = []
        session['attempts'] = (len(rndm_pokemon.name.upper()) // 2) - 1
    else:
        rndm_pokemon_id = session['rndm_pokemon_id']
        rndm_pokemon = Pokemon.query.get(rndm_pokemon_id)

    """ all_pokemon = Pokemon.query.all()
    rndm_pokemon = random.choice(all_pokemon) """

    # Hangman mechanic
    pokemon_name = rndm_pokemon.name.upper()
    guessed_chars = session.get('guessed_chars', [])
    letters = session.get('letters', list(string.ascii_uppercase))
    attempts = (len(pokemon_name) // 2) - 1
    if attempts < 1:
        attempts = 2

    regex_sub = '_' * len(pokemon_name)  # Default value for regex_sub (ChatGPT)

    if request.method == 'POST':
        if attempts < 0:
            reset_game()
            return redirect(url_for('game'))
            # Render template or pop up to play again

        regex = r'[^ '+ "".join(guessed_chars) + r']'  # Dynamic regex list (ChatGPT)
        regex_sub = re.sub(regex, '_', pokemon_name)
        if regex_sub == pokemon_name:
            # If user add to collection PokemonMaster
            # Render template or pop up to play again
            ...

        letter = request.form.get('guess').upper()
        if letter in pokemon_name:
            guessed_chars.append(letter) 
        else:
            attempts -= 1

        if letter in letters:
            letters.remove(letter)

    session['letters'] = letters
    session['guessed_chars'] = guessed_chars

    return render_template(
        'game.html', 
        rndm_pokemon=rndm_pokemon, 
        masked_word=regex_sub, 
        letters=letters,
        attempts=attempts
    )

def reset_game():
    session.pop('rndm_pokemon_id', None)
    session.pop('letters', None)
    session.pop('guessed_chars', None)
    session.pop('attempts', None)

if __name__ == '__main__':
    app.run(debug=True)