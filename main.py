from flask import Flask, render_template

# Create a Flask app
app = Flask(__name__)

# Create a route decorator
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

#Create custom error pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

# Internal server error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500