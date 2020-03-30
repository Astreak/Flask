from flask import *
from flask_sqlalchemy import *
from f import Register,Login
from flask_migrate import Migrate

import os
app=Flask(__name__)
app.config["SECRET_KEY"]="ANYTHING"
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:MYPASSWORD@localhost:3306/practice"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
db=SQLAlchemy(app)
migrate=Migrate(app,db)

class User(db.Model):
	__tablename__="USER"
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(100),unique=True,nullable=False)
	email=db.Column(db.String(100),unique=True,nullable=False)
	image=db.Column(db.String(600),unique=False,nullable=False)
	password=db.Column(db.String(1000),unique=False,nullable=False)
	details=db.relationship("Details",backref="Mapper",lazy=True)

class Details(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	Address=db.Column(db.String(100),unique=True,nullable=False)
	Housename=db.Column(db.String(100),unique=True,nullable=False)
	City=db.Column(db.String(1000),unique=False,nullable=False)
	Uni=db.Column(db.String(100),unique=False,nullable=False)
	users=db.Column(db.Integer,db.ForeignKey("USER.id"))



@app.route("/")
@app.route("/<mode>")
def index(mode=None):
	if mode =="Dark":
		session["mode"]=True
	else:
		session["mode"]=False
	return render_template("index.html",mode=session.get("mode"))

@app.route("/register",methods=["GET","POST"])
def register():
	form=Register()
	if form.validate_on_submit():
		users=User(username=form.username.data,email=form.email.data,password=form.password.data,image=form.file.data.filename)
		
		file=form.file.data
		extension=file.filename.split(".")
		path=os.path.join(os.getcwd(),file.filename)
		path=os.rename(path,os.path.join(os.getcwd(),"file."+extension[1]))
		file.save(os.path.join(os.getcwd(),"file.jpg"))
		print(file)
		db.session.add(users)
		db.session.commit()
		return redirect (url_for("details",mode=session.get("mode")))
	return render_template("register.html",mode=session.get("mode"),form=form)

@app.route("/details",methods=["POST","GET"])
def details():
	if request.method=="POST":
		Data=request.form["username"]
		user=User.query.filter_by(username=Data).first()
		if user:
			details=Details(Address=request.form["add"],Housename=request.form["house"],City=request.form["city"],Uni=request.form["university"],users=user.id)		
			db.session.add(details)
			db.session.commit()
			return redirect(url_for("status",n="YOU ARE SUCCESSFULLY REGISterd and part of our family"))
		else:
			return redirect(url_for("status",n="THERE HAS TO BE SOME PROBLEM CHECK AGAIN"))
	return render_template("details.html",mode=session.get("mode"))
@app.route("/status/<n>")
def status(n):
	return render_template("status.html",mode=session.get("mode"),n=n)

@app.route("/internal_things")
def take_info():
	k=input("ENTER THE NAME")
	Q=User.query.filter_by(username=k).first()
	A=Q.details[0]
	print(A.query.all())
	return redirect(url_for("index",mode=session.get("mode")))

@app.route("/login",methods=["GET","POST"])
def login():
	form=Login()
	if form.validate_on_submit():
		D=User.query.filter_by(email=form.email.data).first()
		
		if D.password==form.password.data:
			data=True
		else:
			data=False
		if data:
			return redirect(url_for("status",mode=session.get("mode"),n="YOU ARE SUCCESSFULLY LOGGED IN"))
		else:
			return redirect(url_for("register",mode=session.get("mode")))
	return render_template("login.html",mode=session.get("mode"),form=form)






	

app.run(debug=True)
