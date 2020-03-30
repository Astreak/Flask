from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired,FileField
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextField
from wtforms.validators import DataRequired,ValidationError,Length,Email,EqualTo
class Register(FlaskForm):
	username=StringField("Username",validators=[DataRequired(),Length(max=100,min=3)])
	email=StringField("Email",validators=[DataRequired(),Email()])
	password=PasswordField("Password",validators=[DataRequired()])
	file=FileField("FILES",validators=[FileRequired()])
	submit=SubmitField("SIgn Up")


class Login(FlaskForm):
	#username=StringField("Username",validators=[DataRequired(),Length(max=100,min=3)])
	email=StringField("Email",validators=[DataRequired(),Email()])
	password=PasswordField("Password",validators=[DataRequired()])
	remember_me=BooleanField("Remember_Me")
	submit=SubmitField("SIgn In")

class Change(FlaskForm):
	#username=StringField("Username",validators=[DataRequired(),Length(max=100,min=3)])
	pass1=PasswordField("New Password",validators=[DataRequired()])
	pass2=PasswordField("Password",validators=[DataRequired(),EqualTo("pass1")])
	#remember_me=BooleanField("Remember_Me")
	submit=SubmitField("change it")
class Follow(FlaskForm):
	name=StringField("USER",validators=[DataRequired()])
	submit=SubmitField("Search",validators=[DataRequired()])

class Posts(FlaskForm):
	Text=TextField("Write",validators=[DataRequired()])
	submit=SubmitField("Post")
	

