from xmlrpc.client import DateTime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug import security


# Create the database interface
db = SQLAlchemy()

# User Model
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120))
    phone_number = db.Column(db.String(80))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    language = db.Column(db.String(80))
    timezone = db.Column(db.String(80))
    currency = db.Column(db.String(80))
    working = db.Column(db.Boolean)
    yearsAtCompany = db.Column(db.Integer)

    technologies = db.relationship('UserTechnology', backref='user', lazy=True)
    department = db.relationship('Department', backref='user', uselist=False)
    projects = db.relationship('UserProjectRelation', backref='user', lazy=True)
    surveys = db.relationship('TeamMemberSurvey', backref='user', lazy=True)


    def __init__(self, username, password, email, phone_number, department_id, language,
                    timezone, currency, working, yearsAtCompany):
        self.username = username
        self.password = password
        self.email = email
        self.phone_number = phone_number
        self.department_id = department_id
        self.language = language
        self.timezone = timezone
        self.currency = currency
        self.working = working
        self.yearsAtCompany = yearsAtCompany

class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    location = db.Column(db.Integer)
    username = db.Column(db.String(80), db.ForeignKey('user.username'))

    def __init__(self, name, location, username):
        self.name = name
        self.location = location
        self.username = username
    
class UserTechnology(db.Model):
    __tablename__ = "user_technology"
    username = db.Column(db.String(20), db.ForeignKey('user.username'), primary_key=True)
    technology_id = db.Column(db.Integer, db.ForeignKey('technology.id'), primary_key=True)
    yearsExperience = db.Column(db.Integer)

    def __init__(self, username, technology_id, yearsExperience):
        self.username = username
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
    name = db.Column(db.String(50), nullable=False)
    manager_username = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
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

    def __init__(self, name, manager_username, budget, deadline, is_completed):
        self.name = name
        self.manager_username = manager_username
        self.budget = budget
        self.deadline = deadline
        self.is_completed = is_completed


class Expense(db.Model):
    __tablename__ = "expense"
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    expense_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

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
    description = db.Column(db.String(100), nullable=False)
    is_implemented = db.Column(db.Boolean, nullable=False)

    def __init__(self, project_id, description, is_implemented):
        self.project_id = project_id
        self.description = description
        self.is_implemented = is_implemented

class ProjectMilestone(db.Model):
    __tablename__ = "project_milestone"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
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
    username = db.Column(db.String(20), db.ForeignKey('user.username'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __init__(self, username, project_id):
        self.username = username
        self.project_id = project_id
    
class TeamMemberSurvey(db.Model):
    __tablename__ = 'team_member_survey'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), db.ForeignKey('user.username'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __init__(self, username, project_id):
        self.username = username
        self.project_id = project_id

class UserProjectRelation(db.Model):
    __tablename__ = 'user_project_relation'
    username = db.Column(db.String(20), db.ForeignKey('user.username'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    is_manager = db.Column(db.Boolean, nullable=False)

    def __init__(self, username, project_id, role):
        self.username = username
        self.project_id = project_id
        self.role = role






# Populate the database with some dummy data
def dbinit():
    user_list = [
        User("Bob", security.generate_password_hash("password"), "email@gmail.com"),
    ]
    db.session.add_all(user_list)

    # Find the id of the user Bob
    bob_id = User.query.filter_by(username="Bob").first().id

    # Commit all the changes to the database file.
    db.session.commit()

