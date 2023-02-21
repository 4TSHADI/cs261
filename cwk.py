from xml.dom import NoModificationAllowedErr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug import security
from markupsafe import escape
from flask import Flask, Response, make_response, render_template, render_template_string, request, redirect, flash, send_file
from sqlalchemy import desc
import os
from datetime import datetime
from sqlalchemy.sql.expression import func

# -------------------------
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


# Database config and import
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
from db_schema import db, User, UserProjectRelation, Expense, ProjectMilestone, dbinit
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
def load_user(username):
    return User.query.get(username)


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
        firstname = escape(request.form.get("firstname"))
        lastname = escape(request.form.get("lastname"))
        email = escape(request.form.get("email"))

        # attempt to add new user to database
        try:
            newUser = User(username=username, password=passwordHash, firstname=firstname, lastname=lastname, email=email, phone_number=None, department_id=None, language=None, timezone=None, currency=None, working=True, yearsAtCompany=None)
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
            return False
        
        if not security.check_password_hash(dbUser.password, password):
            print("password doesn't match")
            return False

        # entered password matches the stored password for the user, login them in
        res = login_user(dbUser)
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
        username = escape(request.form.get("username"))
        password = escape(request.form.get("password"))

        # Attempt to login
        if makeLogin(username, password):
            print("login successful")
            return redirect("/")
        else:
            flash("Unable to login", "error")
            return redirect("/login")
    
    if request.method == "GET":
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    # If a user is logged in, then log them out.
    if current_user.is_authenticated:
        logout_user()
    return redirect("/")

@app.route("/expenses", methods=["GET", "POST"])
def expenses():
    if request.method == "POST":
        title = escape(request.form.get("expTitle"))
        description = escape(request.form.get("expDescription"))
        amount = request.form.get("expAmount")
        date = request.form.get("expDate")

        # carry out length checking in JS
        # REMOVE HARDCODED VALUES
        try: 
            projectID = 1 # hardcoded for now - need to pass actual pid in
            userRole = UserProjectRelation.query.filter_by(user_id=8, project_id=1).first().role

            if userRole.lower() in ["project manager", "business analyst"]:
                prev_expense_id = db.session.query(func.max(Expense.expense_id)).first()[0]
                if prev_expense_id == None: prev_expense_id = 0
                new_expense = Expense(project_id=projectID, expense_id=prev_expense_id+1, name=title, 
                description=description, amount=amount, timestamp=datetime.strptime(date, '%Y-%m-%d'))
                db.session.add(new_expense)
                db.session.commit()

            flash("Expense created!", category="success")
        except:
            flash("Expense could not be created!", category="error")
    return render_template("expenses.html")


@app.route("/milestones", methods=["GET", "POST"])
def milestones():
    if request.method == "POST":
        title = escape(request.form.get("milTitle"))
        description = escape(request.form.get("milDescription"))
        date = request.form.get("milDate")

        # carry out length checking in JS
        # REMOVE HARDCODED VALUES
        #try: 
        projectID = 1 # hardcoded for now - need to pass actual pid in
        userRole = UserProjectRelation.query.filter_by(user_id=8, project_id=projectID).first().role
        if userRole.lower() in ["project manager", "business analyst"]:
            new_milestone = ProjectMilestone(project_id=projectID, title=title,description=description,
            deadline=datetime.strptime(date, '%Y-%m-%d'), completed_date=None )
            db.session.add(new_milestone)
            db.session.commit()
            flash("Milestone created!", category="success")
        # except:
        #     pass
    return render_template("milestones.html")