from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
#from app import db
db = SQLAlchemy()
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    username=db.Column(db.String(100))
    
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    hashed_pswd = db.Column(db.String(), nullable=False)

def init_db():
    db.create_all()

if __name__ == '__main__':
    init_db()

