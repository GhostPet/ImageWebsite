from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, EmailField, TelField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField

class UserForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	username = StringField('Username', validators=[DataRequired()])
	email = EmailField('Email', validators=[DataRequired()])
	phone = TelField('Phone')
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match!')])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
	submit = SubmitField('Submit')

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Submit')

class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	#content = StringField('Content', validators=[DataRequired()], widget=TextArea())
	content = CKEditorField('Content', validators=[DataRequired()])
	author = StringField('Author')
	slug = StringField('Slug', validators=[DataRequired()])
	submit = SubmitField('Submit')

class SearchForm(FlaskForm):
	query = StringField('Search', validators=[DataRequired()])
	submit = SubmitField('Submit')