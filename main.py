from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a Flask app
app = Flask(__name__)
# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Add secret key
app.config['SECRET_KEY'] = "wow-so-secret lol"
# Initialize the database
db = SQLAlchemy(app)

# Create a model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name

# Create a form class
class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Create a form class
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Create a route decorator
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    name = None
    email = None
    form = UserForm()
    if form.validate_on_submit():
        new_user = User.query.filter_by(email=form.email.data).first()
        if new_user is None:
            user = User(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
            flash('User added successfully.', 'success')
        else:
            flash('User already exists.', 'warning')
        name = form.name.data
        email = form.email.data
        form.name.data = ''
        form.email.data = ''
    users = User.query.all()
    return render_template('add_user.html', form=form, name=name, email=email, users=users)

# Create name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Form submitted successfully.')
    return render_template('name.html', name=name, form=form)

#Create custom error pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

# Internal server error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500