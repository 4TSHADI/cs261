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
    username = db.Column(db.String(50), primary_key = True)
    password = db.Column(db.Text())
    firstname = db.Column(db.Text())
    lastname = db.Column(db.Text())
    email = db.Column(db.Text(), unique = True)
    phoneNumber = db.Column(db.String(15), unique = True)
    departmentID = db.Column(db.Integer)
    language = db.Column(db.String(20)) # Not sure how we are going to store/use this.
    timezone = db.Column(db.String(20)) # Not sure how we are going to store/use this.
    currency = db.Column(db.String(10)) # Not sure how we are going to store/use this.
    working = db.Column(db.Boolean) # Boolean of if they are currently working, e.g. False = on holiday.
    yearsAtCompany = db.Column(db.Integer)


    def __init__(self, username, password, firstname, lastname, email, phoneNumber, departmentID, language, timezone, currency, working, yearsAtCompany):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phoneNumber = phoneNumber
        self.departmentID = departmentID
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

