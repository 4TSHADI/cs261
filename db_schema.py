from xmlrpc.client import DateTime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug import security
import datetime



# Create the database interface
db = SQLAlchemy()

# User Model
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    password = db.Column(db.String(80))
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(120), unique = True)
    phone_number = db.Column(db.String(80))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    language = db.Column(db.String(80)) # TODO: change so it references the language table
    timezone = db.Column(db.String(80))
    currency = db.Column(db.String(80))
    working = db.Column(db.Boolean)
    yearsAtCompany = db.Column(db.Integer)
    profile_image_path = db.Column(db.String(100))

    technologies = db.relationship('UserTechnology', backref='user', lazy=True)
    department = db.relationship('Department', backref='user', uselist=False)
    projects = db.relationship('UserProjectRelation', backref='user', lazy=True)
    surveys = db.relationship('TeamMemberSurvey', backref='user', lazy=True)


    def __init__(self, username, password, firstname, lastname, email, phone_number, department_id, language,
                    timezone, currency, working, yearsAtCompany, profile_image_path="./static/images/uploads/profiles/default.png"):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone_number = phone_number
        self.department_id = department_id
        self.language = language
        self.timezone = timezone
        self.currency = currency
        self.working = working
        self.yearsAtCompany = yearsAtCompany
        self.profile_image_path = profile_image_path

class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    location = db.Column(db.Integer)

    def __init__(self, name, location):
        self.name = name
        self.location = location
    
class UserTechnology(db.Model):
    __tablename__ = "user_technology"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    technology_id = db.Column(db.Integer, db.ForeignKey('technology.id'), primary_key=True)
    yearsExperience = db.Column(db.Integer)

    def __init__(self, user_id, technology_id, yearsExperience):
        self.user_id = user_id
        self.technology_id = technology_id
        self.yearsExperience = yearsExperience

class Technology(db.Model):
    __tablename__ = "technology"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    user_technologies = db.relationship('UserTechnology', backref='technology', lazy=True)
    project_technologies = db.relationship('ProjectTechnology', backref='technology', lazy=True)

    def __init__(self, name):
        self.name = name

class ProjectTechnology(db.Model):
    __tablename__ = "project_technology"
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    technology_id = db.Column(db.Integer, db.ForeignKey('technology.id'), primary_key=True)
    
    def __init__(self, project_id, technology_id):
        self.project_id = project_id
        self.technology_id = technology_id

class Project(db.Model):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    is_completed = db.Column(db.Boolean, nullable=False)

    technologies = db.relationship('ProjectTechnology', backref='project')
    expenses = db.relationship('Expense', backref='project', lazy=True)
    suggestions = db.relationship('Suggestion', backref='project', lazy=True)
    milestones = db.relationship('ProjectMilestone', backref='project', lazy=True)
    manager_surveys = db.relationship('ProjectManagerSurvey', backref='project', lazy=True)
    team_member_surveys = db.relationship('TeamMemberSurvey', backref='project', lazy=True)
    user_project_relations = db.relationship('UserProjectRelation', backref='project', lazy=True)

    def __init__(self, name, manager_id, budget, deadline, is_completed):
        self.name = name
        self.manager_id = manager_id
        self.budget = budget
        self.deadline = deadline
        self.is_completed = is_completed


class Expense(db.Model):
    __tablename__ = "expense"
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    expense_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False)

    def __init__(self, project_id, expense_id, name, description, amount, timestamp):
        self.project_id = project_id
        self.expense_id = expense_id
        self.name = name
        self.description = description
        self.amount = amount
        self.timestamp = timestamp

class Suggestion(db.Model):
    __tablename__ = "suggestion"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    is_implemented = db.Column(db.Boolean, nullable=False)

    def __init__(self, project_id, description, is_implemented):
        self.project_id = project_id
        self.description = description
        self.is_implemented = is_implemented

class ProjectMilestone(db.Model):
    __tablename__ = "project_milestone"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    completed_date = db.Column(db.DateTime)

    def __init__(self, project_id, title, description, deadline, completed_date):
        self.project_id = project_id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.completed_date = completed_date

class ProjectManagerSurvey(db.Model):
    __tablename__ = "project_manager_survey"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    # TODO: add metrics we gather from survey here

    def __init__(self, user_id, project_id):
        self.user_id = user_id
        self.project_id = project_id
    
class TeamMemberSurvey(db.Model):
    __tablename__ = 'team_member_survey'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    experience = db.Column(db.Float, nullable=False)
    working_environment = db.Column(db.Float, nullable=False)
    hours_worked = db.Column(db.Integer, nullable=False)
    communication = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now())

    def __init__(self, user_id, project_id, experience, working_environment, hours_worked, communication, timestamp):
        self.user_id = user_id
        self.project_id = project_id
        self.experience = experience
        self.working_environment = working_environment
        self.hours_worked = hours_worked
        self.communication = communication
        self.timestamp = timestamp


class UserProjectRelation(db.Model):
    __tablename__ = 'user_project_relation'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    is_manager = db.Column(db.Boolean, nullable=False)
    role = db.Column(db.String(80), nullable=False)

    def __init__(self, user_id, project_id, is_manager, role):
        self.user_id = user_id
        self.project_id = project_id
        self.is_manager = is_manager
        self.role = role


class Language(db.Model):
    __tablename__ = 'language'
    name = db.Column(db.String(20), primary_key=True)

    def __init__(self, name):
        self.name = name
    
class Timezone(db.Model):
    __tablename__ = 'timezone'
    name = db.Column(db.String(20), primary_key=True)

    def __init__(self, name):
        self.name = name

class Currency(db.Model):
    __tablename__ = 'currency'
    name = db.Column(db.String(20), primary_key=True)

    def __init__(self, name):
        self.name = name

    


# This function is called when the database is reset (resetdb boolean=True in cwk.py file)
# Put code in here to populate the database with dummy values.
def dbinit():
    user_list = [ # TODO: change this to be dummy data for the new user schema
        User("Mike18", security.generate_password_hash("password"), "Michael", "Cooper", "michael@tedxwarwick.com", "07732444444", 1, "en", "GMT+0", "£", True, 7),
        User("Bob24", security.generate_password_hash("password"), "Bob", "Jones", "Bob@tedxwarwick.com", "07732645287", 2, "en", "GMT+0", "£", True, 7)
    ]
    
    db.session.add_all(user_list)

    # Find the id of the user Bob
    # bob_id = User.query.filter_by(username="Bob").first().id
    project_list = [
        Project("Project A", 1, 100000, func.now(), False),
        Project("Project B", 2, 10, func.now(), False),
        Project("Project C", 2, 999, func.now(), False),
        Project("Project D", 1, 4568, func.now(), False),
    ]
    db.session.add_all(project_list)

    userProjectRelaion_list = [
        UserProjectRelation(1, 1, False, "Software Engineer"),
        UserProjectRelation(1, 2, True, "Project Manager"),
        UserProjectRelation(1, 3, False, "Software Engineer"),
        UserProjectRelation(2, 1, True, "Project Manager"),
        UserProjectRelation(2, 2, False, "Software Engineer")
    ]
    db.session.add_all(userProjectRelaion_list)


    department_list = [
        Department("Frontend", 1),
        Department("Security", 1),
        Department("API", 2),
        Department("Backend", 3)
    ]
    db.session.add_all(department_list)

    languages = ["English", "French", "Spanish", "German"]
    languages_list = [Language(x) for x in languages]
    db.session.add_all(languages_list)

    timezones = [("GMT" + str(a) + str(n)) for a in ["+", "-"] for n in range(12)]
    timezone_list = [Timezone(x) for x in timezones]
    db.session.add_all(timezone_list)

    currencies = ["£", "$", "€", "¥"]
    currency_list = [Currency(x) for x in currencies]
    db.session.add_all(currency_list)

    technologies = ["Python", "HTML", "SQLite", "SaaS", "Jinja", "AWS", "Azure"]
    technology_list = [Technology(x) for x in technologies]
    db.session.add_all(technology_list)


    # Commit all the changes to the database file.
    db.session.commit()

