from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

print("Database path:", os.path.abspath("users.db"))

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        print(f"New user signed up: {username}, {email}, {password}")

        if password != password2:
            flash("Passwords do not match.")
            return redirect(url_for('signup'))

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or email already exists.")
            return redirect(url_for('signup'))

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created! Please log in.")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user'] = user.username
            return redirect(url_for('dashboard'))
        flash("Invalid credentials.")
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/all-users')
def show_users():
    users = User.query.all()
    return '<br>'.join([f"{u.id} - {u.username} - {u.email}" for u in users])



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Absolute DB path:", os.path.abspath("users.db"))

    app.run(debug=True)
