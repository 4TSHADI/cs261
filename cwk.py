from aifc import Error
from xml.dom import NoModificationAllowedErr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug import security
from werkzeug.utils import secure_filename
from markupsafe import escape
from flask import Flask, Response, make_response, render_template, render_template_string, request, redirect, flash, send_file
from sqlalchemy import desc
from datetime import datetime, timedelta
import os
from datetime import datetime
from sqlalchemy.sql.expression import func

# -------------------------
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# User file upload config
UPLOAD_FOLDER = "./static/images/uploads/profiles"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_UPLOAD_LENGTH"] = 4 * 1024 * 1024 # Set max file upload size to be 4 MB


# Database config and import
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
from db_schema import db, User, Department, UserTechnology, Technology, ProjectTechnology, Project, Expense, Suggestion, ProjectMilestone, ProjectManagerSurvey, TeamMemberSurvey, UserProjectRelation, Language, Timezone, Currency, dbinit
db.init_app(app)

resetdb = True  # Change to True to reset the database with the data defined in the db_schema.py file.
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
            newUser = User(username=username, password=passwordHash, firstname=firstname, lastname=lastname, email=email, phone_number="444444444", department_id=1, language=None, timezone=None, currency=None, working=True, yearsAtCompany=None)
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
@login_required
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
@login_required
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

@app.route("/profile")
@login_required
def profile():
    if request.method == "GET":

        user_department_id = User.query.get(current_user.id).department_id
        user_department = Department.query.get(user_department_id)
        
        user_projects = db.session.query(Project).join(UserProjectRelation)\
            .filter(Project.id == UserProjectRelation.project_id, UserProjectRelation.user_id == current_user.id).all()
        # print("projects: " + str(user_projects1))


        return render_template("profile.html", user_department=user_department, user_projects=user_projects)


@app.route("/edit_profile", methods=["POST", "GET"])
@login_required
def edit_profile():
    if request.method == "POST":
        # Handle updating of user details.
        username = request.form.get("username")
        new_firstname = request.form.get("firstname")
        new_lastname = request.form.get("lastname")
        new_email = request.form.get("email")
        new_phone_number = request.form.get("phone_number")
        new_department_id = request.form.get("department")
        new_language = request.form.get("language")
        new_timezone = request.form.get("timezone")
        new_currency = request.form.get("currency")
        new_working = request.form.get("working")
        new_years_at_company = request.form.get("years_at_company")

        # Check user with the same email doesn't already exist.
        user_email_test = db.session.query(User).filter(User.email == new_email).first()
        if user_email_test is not None and current_user.email != new_email:
            # Email already exists in database.
            print("email already exists in database")
            flash("New email already in use", "error")
            return redirect("/profile")
    

        user_data =  db.session.query(User).filter(User.username == current_user.username).first()
        if user_data is None:
            print("error, user doesn't exist")
            flash("Unable to update details", "error")
            return redirect("/profile")

        # Update user_data values in the database
        try:
            user_data.firstname = new_firstname
            user_data.lastname = new_lastname
            user_data.email = new_email
            user_data.phone_number = new_phone_number
            user_data.department_id = new_department_id
            user_data.language = new_language
            user_data.timezone = new_timezone
            user_data.currency = new_currency
            user_data.working = True if new_working == "True" else False
            user_data.yearsAtCompany = new_years_at_company

            
            db.session.commit()
        except Exception as e:
            print(e)
            print("error updating user")
            flash("Unable to update details", "error")
            return redirect("/profile")

        # ----- Getting user profile image -----
        # Check image file has been submitted
        if "image_file" not in request.files:
            flash("No file submitted", "error")
            return redirect(request.url)
        
        image_file = request.files["image_file"]

        # Addition checks user has selected a file.
        if not image_file or image_file.filename == "":
            flash("No file submitted", "error")
            return redirect(request.url)
        
        # Check file extension
        if "." not in image_file.filename:
            flash("Invalid file uploaded")
            return redirect(request.url)
        file_extension = image_file.filename.rsplit(".", 1)[1].lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            flash("Invalid file uploaded", "error")
            return redirect(request.url)
        
        # Make filename the users username plus appropriate extension
        # Overwrites file if already exists.
        filename = secure_filename(current_user.username + "." + file_extension)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image_file.save(filepath)

        # Insert file path into User table in database
        user_data.profile_image_path = filepath
        db.session.commit()
        
        flash("User details updated", "info")
        return redirect("/profile")

    elif request.method == "GET":
        departments = db.session.query(Department).all()
        languages = db.session.query(Language).all()
        timezones = db.session.query(Timezone).all()
        currencies = db.session.query(Currency).all()

        return render_template("edit_profile.html", departments=departments, languages=languages, timezones=timezones, currencies=currencies)


@app.route("/add_technology", methods=["POST", "GET"])
@login_required
def add_technology():
    if request.method == "POST":
        technology = request.form.get("technology")

        # Check if technology already exists in database
        exists = db.session.query(Technology).filter(Technology.name == technology).first()
        if exists is not None:
            print("Technology already exists in the database")
            flash("Technology already exists", "message")
            return redirect(request.referrer)

        # Add new technology to database
        try:
            new_technology = Technology(technology)
            db.session.add(new_technology)
            db.session.commit()
            flash("Technology added", "info")
        except:
            print("Error, unable to add technology")
            flash("Unable to add technology", "error")
            return redirect(request.referrer)

        return redirect(request.referrer)
    elif request.method == "GET":

        return render_template("add_technology.html")

@app.route("/user_technology", methods=["POST", "GET"])
@login_required
def user_technology():
    if request.method == "POST":
        technologies = db.session.query(Technology).all()
        years = [[tech.id, tech.name, request.form.get(str(tech.id))] for tech in technologies]
        
        try:
            # loop through zip of technologies and collected years experience
            for entry in years:
                id = entry[0]
                name = entry[1]
                years_exp = entry[2]

                # Get row from database
                row = db.session.query(UserTechnology).filter(UserTechnology.user_id==current_user.id, UserTechnology.technology_id==id).first()
                if row is not None: # if row exists, update years value.
                    # print("Row for " + name + " exists, updating value")
                    row.yearsExperience = years_exp

                else: # if row doesnt exist, create and insert
                    # print("Row for " + name + " doesn't exist, creating row")
                    new_row = UserTechnology(current_user.id, id, years_exp)
                    db.session.add(new_row)

            db.session.commit()
        except:
            print("error - user tech")
            flash("Unable to update technologies", "error")
            return redirect("/profile")

        print("user technologies updated")
        flash("Technologies updated", "message")
        return redirect("/profile")
    
    elif request.method == "GET":
        user_id = current_user.id
        technologies = db.session.query(Technology).all()
        
        technology_list = []
        for technology in technologies:
            row  = db.session.query(UserTechnology).filter(UserTechnology.user_id == user_id, UserTechnology.technology_id == technology.id).first()
            # print(row)

            years_experience = row.yearsExperience if row else 0

            tech_info = {"technology_id": technology.id, "name": technology.name, "years": years_experience}
            technology_list.append(tech_info)
        
        # print(technology_list)

        return render_template("user_technology.html", technologies = technology_list)


@app.route("/survey", methods=["GET","POST"])
@login_required
def survey():
    project_id = request.form.get("project_id")
    this_monday = datetime.utcnow().date() - timedelta(days=datetime.utcnow().date().weekday())
    next_monday = this_monday + timedelta(weeks=1)

    existing_survey = TeamMemberSurvey.query.filter_by(user_id=current_user.id, project_id=project_id).filter(TeamMemberSurvey.timestamp >= this_monday).first()
    print(existing_survey)
    if request.method == "POST":
        # Get form fields
        experience = escape(request.form.get("experience"))
        working_environment = escape(request.form.get("working_environment"))
        hours_worked = escape(request.form.get("hours_worked"))
        communication = escape(request.form.get("communication"))

        # Store survey results in database 
        new_survey = TeamMemberSurvey(current_user.id, project_id, experience=str(experience), working_environment=str(working_environment), hours_worked=str(hours_worked), communication=str(communication),timestamp=datetime.utcnow())        
        db.session.add(new_survey)
        db.session.commit()

        return redirect("/")
    if existing_survey:
        print("HELLOLOFEJFOEJFOJE")
        return render_template("survey_not_available.html", next_monday=next_monday)
    else:
        return render_template('survey.html', project_id=project_id)
