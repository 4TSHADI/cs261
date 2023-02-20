from xml.dom import NoModificationAllowedErr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug import security
from markupsafe import escape
from flask import Flask, Response, make_response, render_template, render_template_string, request, redirect, flash, send_file
from sqlalchemy import desc
import os

# -------------------------
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


# Database config and import
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
from db_schema import db, User, dbinit
db.init_app(app)

resetdb = True # Change to True to reset the database with the data defined in the db_schema.py file.
if resetdb:
    with app.app_context():
        # Drop everything, create all tables and populate with data
        db.drop_all()
        db.create_all()
        dbinit()


# Import login manager
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login" # sets the route to go to if the user attempts to access a route which requries them to be logged in and they are not.

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


# Routes
@app.route('/')
@login_required
def index(): 
    return render_template('home.html')



@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        # already logged in
        return redirect("/")

    if request.method == "POST":
        # Get the form fields.
        username = escape(request.form.get("username"))
        password = escape(request.form.get("password"))
        passwordHash = security.generate_password_hash(password)
        email = escape(request.form.get("email"))

        # attempt to add new user to database
        try:
            newUser = User(username=username, password=passwordHash, email=email)
            db.session.add(newUser)
            db.session.commit()

        except IntegrityError as exc:
            db.session.rollback()
            flash("Could not register user!", "error")
            return redirect("/register")
        
        makeLogin(username, password) # Logs the user in with the details they provided
        return redirect("/")

    if request.method == "GET":
        return render_template("register.html")


def makeLogin(username, password):
    try:
        # Get the user with the entered username
        dbUser = User.query.filter_by(username=username).first()
        if dbUser is None:
            print("User doesn't exist.")
            return redirect("/login")
        
        if not security.check_password_hash(dbUser.password, password):
            print("password doesn't match")
            return redirect("/login")

        # entered password matches the stored password for the user, login them in
        login_user(dbUser)
        # print("user " + username + " logged in")
        return True

    except:
        return False


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        # already logged in.
        return redirect("/")

    if request.method == "POST":
        # Get form fields.
        username = request.form.get("username")
        password = request.form.get("password")

        # Attempt to login
        if makeLogin(username, password):
            return redirect("/")
        else:
            flash("Unable to login", "error")
            return redirect("/login")
    
    if request.method == "GET":
        return render_template("home.html")


@app.route("/logout")
@login_required
def logout():
    # If a user is logged in, then log them out.
    if current_user.is_authenticated:
        logout_user()
    return redirect("/")

