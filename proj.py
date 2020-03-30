from flask import *
from flask_sqlalchemy import *
app=Flask(__name__)
app.config["SECRET_KEY"]="ANYTHING"
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:MYPASSWORD@localhost:3306/practice"
db=SQLAlchemy(app)
class User(db.Model):
	__tablename__="USER"
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(100),unique=True,nullable=False)
	email=db.Column(db.String(100),unique=True,nullable=False)
	password=db.Column(db.String(1000),unique=False,nullable=False)
	details=db.relationship("Details",backref="Mapper",lazy=True)

class Details(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	Address=db.Column(db.String(100),unique=True,nullable=False)
	Housename=db.Column(db.String(100),unique=True,nullable=False)
	City=db.Column(db.String(1000),unique=False,nullable=False)
	Uni=db.Column(db.String(100),unique=False,nullable=False)
	users=db.Column(db.Integer,db.ForeignKey("USER.id"),nullable=False)
from main import *



