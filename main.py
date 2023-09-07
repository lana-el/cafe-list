from flask import Flask, render_template, url_for, redirect, request, flash, abort
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
import sqlite3 
from form import CafeForm, RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_gravatar import Gravatar
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Lan457078'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

with app.app_context():
    db.create_all()

# #Create admin-only decorator
# def admin_only(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         #If id is not 1 then return abort with 403 error
#         if current_user.id != 1:
#             return abort(403)
#         #Otherwise continue with the route function
#         return f(*args, **kwargs)
#     return decorated_function


@app.route("/")
def home(): 
    return render_template("index.html")

@app.route('/cafes')
def cafes():
    conn = sqlite3.connect('instance/cafes.db')
    cursor = conn.cursor()

    # SQL query to retrieve data
    sql = "SELECT id, name, map_url, img_url, location, has_sockets, has_toilet, has_wifi, can_take_calls, seats, coffee_price FROM cafe"
    cursor.execute(sql)
    all_cafes = cursor.fetchall()

    # Close database connection
    conn.close()
    return render_template("cafes.html", cafes=all_cafes)

@app.route('/add', methods=['GET', 'POST'])
# @admin_only
def add():
    form = CafeForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('instance/cafes.db')
        cursor = conn.cursor()

        #SQL query to insert data into the table
        insert_query = "INSERT INTO cafe (name, map_url, img_url, location, has_sockets, has_toilet, has_wifi, can_take_calls, seats, coffee_price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        # Sample data to insert
        new_cafe_data = {
            'name': form.name.data,
            'map_url': form.map_url.data,
            'img_url': form.img_url.data,
            'location': form.location.data,
            'has_sockets': form.has_sockets.data,
            'has_toilet': form.has_toilet.data,
            'has_wifi': form.has_wifi.data,
            'can_take_calls': form.can_take_calls.data,
            'seats':form.seats.data,
            'coffee_price': f'£{form.coffee_price.data}'
        }

        # Execute the insert query with data
        cursor.execute(insert_query, (
            new_cafe_data['name'],
            new_cafe_data['map_url'],
            new_cafe_data['img_url'],
            new_cafe_data['location'],
            new_cafe_data['has_sockets'],
            new_cafe_data['has_toilet'],
            new_cafe_data['has_wifi'],
            new_cafe_data['can_take_calls'],
            new_cafe_data['seats'],
            new_cafe_data['coffee_price'],
        ))
        conn.commit()
        conn.close()

        return redirect(url_for('cafes'))
    return render_template("add.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            print(User.query.filter_by(email=form.email.data).first())
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('register.html', form=form, current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data

        user=User.query.filter_by(email=email).first()
        if not user:
            flash('That email does not exist, please try again.')
            return redirect(url_for('login'))
            # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', form=form, current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)