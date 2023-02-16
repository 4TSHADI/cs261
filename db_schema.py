from xmlrpc.client import DateTime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug import security


# Create the database interface
db = SQLAlchemy()

# User Model
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True) # Let Chris know that had to put id back in the database
    username = db.Column(db.String(80), unique = True)
    password = db.Column(db.String(80))
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(120))
    phone_number = db.Column(db.String(80))
    # department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department_id = db.Column(db.Integer)
    language = db.Column(db.String(80))
    timezone = db.Column(db.String(80))
    currency = db.Column(db.String(80))
    working = db.Column(db.Boolean)
    yearsAtCompany = db.Column(db.Integer)

    # technologies = db.relationship('UserTechnology', backref='user', lazy=True)
    # department = db.relationship('Department', backref='user', uselist=False)
    # projects = db.relationship('UserProjectRelation', backref='user', lazy=True)
    # surveys = db.relationship('TeamMemberSurvey', backref='user', lazy=True)


    def __init__(self, username, password, firstname, lastname, email, phone_number, department_id, language,
                    timezone, currency, working, yearsAtCompany):
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





# This function is called when the database is reset (resetdb boolean=True in cwk.py file)
# Put code in here to populate the database with dummy values.
def dbinit():
    user_list = [
        User("Bob24", security.generate_password_hash("password"), "Bob", "Jones", "email@gmail.com", "07732444444", 1, "en", "GMT+0", "£", True, 5),
    ]
    db.session.add_all(user_list)

    # Find the id of the user Bob
    bob_id = User.query.filter_by(username="Bob24").first().username

    # Commit all the changes to the database file.
    db.session.commit()

