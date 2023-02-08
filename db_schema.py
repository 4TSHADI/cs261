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
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text(), unique = True)
    password = db.Column(db.Text())
    email = db.Column(db.Text())

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email





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

