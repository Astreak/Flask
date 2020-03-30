from flask import *
from flask_sqlalchemy import *
from f import Register,Login,Change,Follow,Posts
from flask_migrate import Migrate
from flask_login import LoginManager,current_user,login_user,login_required,UserMixin,logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import pyrebase
from datetime import datetime

import os
app=Flask(__name__)
app.config["SECRET_KEY"]="ANYTHING"
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:MYPASSWORD@localhost:3306/practice"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
db=SQLAlchemy(app)
migrate=Migrate(app,db)
login=LoginManager(app)

follower = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('USER.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('USER.id'))
)

					
class User(db.Model,UserMixin):
	__tablename__="USER"
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(100),unique=True,nullable=False)
	email=db.Column(db.String(100),unique=True,nullable=False)
	password=db.Column(db.String(1000),unique=False,nullable=False)

	details=db.relationship("Details",backref="Mapper",lazy=True)
	posts=db.relationship("Post",backref="author",lazy=True)
	followed=db.relationship("User",secondary=follower,primaryjoin=(follower.c.follower_id==id),secondaryjoin=(follower.c.followed_id==id),
				backref=db.backref("followers",lazy=True),lazy=True)


	def following_posts(self):
		follow=Post.query.join(follower,(follower.c.followed_id==Post.Us)).filter(follower.c.follower_id==self.id)
		own=Post.query.filter_by(Us=self.id)

		
		return follow.union(own).order_by(Post.timestamp.asc())






class Details(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	Address=db.Column(db.String(100),unique=True,nullable=False)
	Housename=db.Column(db.String(100),unique=True,nullable=False)
	City=db.Column(db.String(1000),unique=False,nullable=False)
	Uni=db.Column(db.String(100),unique=False,nullable=False)
	image=db.Column(db.String(600),unique=False,nullable=True)
	users=db.Column(db.Integer,db.ForeignKey("USER.id"))

class Post(db.Model,UserMixin):
	id=db.Column(db.Integer,primary_key=True)
	content=db.Column(db.String(1000),nullable=False,unique=True)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	Us=db.Column(db.Integer,db.ForeignKey("USER.id"))








@login.user_loader
def validate(user):
	return User.query.get(int(user))


@app.route("/")
@app.route("/<mode>")
@login_required
def index(mode=None):
	
	if mode =="Dark":
		session["mode"]=True
	else:
		session["mode"]=False
	return render_template("index.html",mode=session.get("mode"),us=current_user.username)

@app.route("/register",methods=["GET","POST"])
def register():
	form=Register()
	if form.validate_on_submit():
		users=User(username=form.username.data,email=form.email.data,password=generate_password_hash(form.password.data))
		session["file"]=form.file.data.filename
		db.session.add(users)
		db.session.commit()
		return redirect (url_for("login",mode=session.get("mode")))
	return render_template("register.html",mode=session.get("mode"),form=form)

@app.route("/details",methods=["POST","GET"])
def details():
	if request.method=="POST":
		Data=request.form["username"]
		user=User.query.filter_by(username=Data).first()
		if user:
			details=Details(Address=request.form["add"],Housename=request.form["house"],City=request.form["city"],Uni=request.form["university"],users=user.id,image=session.get("file"))		
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
	
	print(current_user.followed)
	print("followers ",end=" ")
	print(current_user.followers)

	return redirect(url_for("index",mode=session.get("mode")))

@app.route("/login",methods=["GET","POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("index"))
	form=Login()
	
	if form.validate_on_submit():
		D=User.query.filter_by(email=form.email.data).first()
		
		if D:
			
			if not check_password_hash(D.password,form.password.data):
				data=False
				session["EMAIL"]=form.email.data
				
				return redirect(url_for("change_password",user=session["EMAIL"]))
			
				
		else:
			return redirect(url_for("register",mode=session.get("mode")))
			
		
		login_user(D,remember=form.remember_me.data)
		
		return redirect(url_for("index",mode=session.get("mode")))
		
	return render_template("login.html",mode=session.get("mode"),form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("login"))
@app.route("/follow",methods=["GET","POST"])
@login_required
def follow():
	text=Follow()
	if text.validate_on_submit():
		d=text.name.data
		D=User.query.filter_by(username=d).first()

		current_user.followed.append(D)
		db.session.commit()
		return redirect(url_for("index"))
	else:
		print("invalid")
	return render_template("follow.html",A=text)


@app.route("/change",methods=["GET","POST"])
@app.route("/change/<user>",methods=["GET","POST"])
def change_password(user=None):
	F=Change()
	if F.validate_on_submit():
		U=User.query.filter_by(email=user).first()
		
		U.password=generate_password_hash(F.pass1.data)
		db.session.commit()
		return redirect(url_for("login",mode=session.get("mode")))
	return render_template("change.html",mode=session.get("mode"),form=F,user=user)




@app.route("/display")
def Display():
	U=User.query.all()
	for i in U:
		print(i.username)
	return redirect(url_for("index"))


@login_required
@app.route("/posts",methods=["GET","POST"])
def posts():
	Content=Posts()
	
	if Content.validate_on_submit():
		text=Content.Text.data
		post=Post(content=text,Us=current_user.id)
		db.session.add(post)
		db.session.commit()
		N=current_user.following_posts()
		db.session.commit()
		H=current_user.following_posts()
		
		
		
		return redirect(url_for("index"))
	return render_template("poster.html",P=Content)

@login_required
@app.route("/blogs")
def Blogs():
	H=current_user.following_posts()
	l=[]
	for i in H:
		L=i.Us
		L=User.query.filter_by(id=L).first()
		L=L.username
		l.append((L,i.content))

	return render_template("message.html",N=l)

@app.errorhandler(401)
def error(error):
	return render_template("failure1.html"),401

@app.errorhandler(500)
def error(error):
	return render_template("failure1.html"),500
	











app.run(debug=True)






















