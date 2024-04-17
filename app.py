from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_ckeditor import CKEditor

from datetime import datetime
from uuid import uuid1
import os

from webforms import UserForm, LoginForm, PostForm, SearchForm

### App Configs
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images/'

## Database
# Sqlite database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# MySQL database
# Example: mysql+pymysql://username:password@localhost/db_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/users_db'
# PostgreSQL database
# Example: postgresql://username:password@localhost/db_name


app.config['SECRET_KEY'] = "wow-so-secret lol"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

## Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

## CKEditor
ckeditor = CKEditor(app)


### Models

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), nullable=False, unique=True)
	name = db.Column(db.String(50), nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	phone = db.Column(db.String(20), nullable=True)
	password_hash = db.Column(db.String(255))
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	posts = db.relationship('Post', backref='author', lazy=True)
	about_me = db.Column(db.Text, nullable=True)
	profile_pic = db.Column(db.String(255), nullable=True)

	@property
	def password(self):
		raise AttributeError('Password is not a readable attribute.')
	
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<Name %r>' % self.name

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	content = db.Column(db.Text, nullable=False)
	#author = db.Column(db.String(255), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255), nullable=False, unique=True)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Title %r>' % self.title

with app.app_context():
	db.create_all()


### Routes

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/admin')
@login_required
def admin():
	if current_user.id != 2:
		flash('You are not allowed to access this page.', 'danger')
		return redirect(url_for('dashboard'))
	return render_template('admin.html')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
	name = None
	form = UserForm()
	if form.validate_on_submit():
		new_user = User.query.filter_by(email=form.email.data).first()
		if new_user is None:
			user = User(
				name=form.name.data,
				username=form.username.data,
				email=form.email.data,
				phone=form.phone.data,
				password_hash=generate_password_hash(form.password.data)
				)
			db.session.add(user)
			db.session.commit()
			flash('User added successfully.', 'success')
		else:
			flash('User already exists.', 'warning')
		name = form.name.data
		form.name.data = ''
		form.username.data = ''
		form.email.data = ''
		form.phone.data = ''
		form.password.data = ''
	users = User.query.all()
	return render_template('add_user.html', form=form, name=name, users=users)

@app.route('/update_user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
	form = UserForm()
	user = User.query.get_or_404(id)
	if request.method == 'POST':
		# Check if the user logged in is the same user
		if current_user.id != user.id:
			flash('You are not allowed to update this user.', 'danger')
			return render_template('update_user.html', form=form, user=user)
		# Check if anything is changed
		if user.name == form.name.data and user.email == form.email.data and user.phone == form.phone.data:
			flash('Nothing to update.', 'warning')
			return render_template('update_user.html', form=form, user=user)
		# Check if required fields is empty
		if form.name.data == '' or form.email.data == '':
			flash('Please fill the required fields.', 'warning')
			return render_template('update_user.html', form=form, user=user)
		# Check if the email already exists
		email = User.query.filter_by(email=form.email.data).first()
		if email is not None and user.id != email.id:
			flash('Email already exists.', 'warning')
			return render_template('update_user.html', form=form, user=user)
		user.name = form.name.data
		user.email = form.email.data
		user.phone = form.phone.data
		try:
			db.session.commit()
			flash('User updated successfully.', 'success')
		except:
			flash('Database Error: User does not updated.', 'danger')
		return render_template('update_user.html', form=form, user=user)
	
	else:
		return render_template('update_user.html', form=form, user=user)
	
@app.route('/delete_user/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
	user = User.query.get_or_404(id)
	form = UserForm()
	# Check if the user logged in is the same user
	if current_user.id != user.id:
		flash('You are not allowed to delete this user.', 'danger')
		users = User.query.all()
		return render_template('add_user.html', form=form, users=users)
	try:
		db.session.delete(user)
		db.session.commit()
		flash('User deleted successfully.', 'success')
	except:
		flash('Database Error: User does not deleted.', 'danger')
	users = User.query.all()
	return redirect('add_user.html', form=form, users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		
		user = User.query.filter_by(username=form.username.data).first()
		if user is None:
			flash('Invalid email or password.', 'danger')
			return render_template('login.html', form=form)
		elif user.verify_password(form.password.data):
			flash('User logged in successfully.', 'success')
			login_user(user)
			return redirect(url_for('dashboard'))
		else:
			flash('Invalid email or password.', 'danger')
			return render_template('login.html', form=form)
		
	else:
		return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('User logged out successfully.', 'success')
	return redirect(url_for('login'))
	
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	form = UserForm()
	user = current_user
	if request.method == 'POST':
		# Check if anything is changed
		if user.username == form.username.data and user.name == form.name.data and user.email == form.email.data and user.phone == form.phone.data and form.about_me.data == user.about_me and form.profile_pic.data is None:
			flash('Nothing to update.', 'warning')
			return render_template('dashboard.html', form=form)
		# Check if required fields is empty
		if form.username.data == '' or form.name.data == '' or form.email.data == '':
			flash('Please fill the required fields.', 'warning')
			return render_template('dashboard.html', form=form)
		# Check if the email already exists
		email = User.query.filter_by(email=form.email.data).first()
		if email is not None and user.id != email.id:
			flash('Email already exists.', 'warning')
			return render_template('dashboard.html', form=form)
		# Check if the username already exists
		username = User.query.filter_by(username=form.username.data).first()
		if username is not None and user.id != username.id:
			flash('Username already exists.', 'warning')
			return render_template('dashboard.html', form=form)
		# Update the user
		user.username = form.username.data
		user.name = form.name.data
		user.email = form.email.data
		user.phone = form.phone.data
		user.about_me = form.about_me.data

		if form.profile_pic.data is not None:
			# Profile Picture
			pic_filename = secure_filename(form.profile_pic.data.filename)
			pic_name = str(uuid1()) + "_" + pic_filename
			user.profile_pic = pic_name
			profile_pic_path = os.path.join(app.config['UPLOAD_FOLDER'], "profile_pics/", pic_name)
			form.profile_pic.data.save(profile_pic_path)		

		try:
			db.session.add(user)
			db.session.commit()
			flash('User updated successfully.', 'success')
		except:
			flash('Database Error: User does not updated.', 'danger')
		form.about_me.data = user.about_me
		return render_template('dashboard.html', form=form)
	
	else:
		form.about_me.data = user.about_me
		return render_template('dashboard.html', form=form)
	
@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(
			title=form.title.data,
			content=form.content.data,
			author_id=current_user.id,
			slug=form.slug.data
			)
		db.session.add(post)
		db.session.commit()
		flash('Post added successfully.', 'success')
		form.title.data = ''
		form.content.data = ''
		form.author.data = ''
		form.slug.data = ''
	posts = Post.query.all()
	return render_template('add_post.html', form=form, posts=posts)

@app.route('/posts')
def posts():
	posts = Post.query.order_by(Post.date_created.desc())
	return render_template('posts.html', posts=posts)

@app.route('/post/<slug>')
def post(slug):
	post = Post.query.filter_by(slug=slug).first_or_404()
	return render_template('post.html', post=post)

@app.route('/post/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(slug):
	post = Post.query.filter_by(slug=slug).first_or_404()
	if current_user.id != post.author_id:
		flash('You are not allowed to edit this post.', 'danger')
		return redirect(url_for('posts'))
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		post.slug = form.slug.data
		try:
			db.session.add(post)
			db.session.commit()
			flash('Post updated successfully.', 'success')
		except:
			flash('Database Error: Post does not updated.', 'danger')
		return redirect(url_for('posts'))
	else:
		form.title.data = post.title
		form.content.data = post.content
		form.slug.data = post.slug
		return render_template('edit_post.html', form=form)
	
@app.route('/post/<slug>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(slug):
	post = Post.query.filter_by(slug=slug).first_or_404()
	if current_user.id != post.author_id:
		flash('You are not allowed to delete this post.', 'danger')
		return redirect(url_for('posts'))
	try:
		db.session.delete(post)
		db.session.commit()
		flash('Post deleted successfully.', 'success')
	except:
		flash('Database Error: Post does not deleted.', 'danger')
	return redirect(url_for('posts'))

@app.context_processor
def base_context():
	search_form = SearchForm()
	return dict(search_form=search_form)

@app.route('/search', methods=['GET', 'POST'])
def search():
	form = SearchForm()
	query = form.query.data
	if form.validate_on_submit():
		posts = Post.query.filter(Post.title.like('%'+query+'%') | Post.content.like('%'+query+'%') ).all()
		return render_template('search.html', posts=posts, form=form)
	else:
		return redirect(url_for('posts'))

## Error Pages

# 404: Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template('errors/404.html'), 404

# 500: Internal server error
@app.errorhandler(500)
def internal_server_error(e):
	return render_template('errors/500.html'), 500