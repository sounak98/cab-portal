# Import flask and template operators
from flask import Flask, render_template, request
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Define the WSGI application object
app = Flask(__name__)
admin = Admin(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

# Configurations
app.config.from_object('config')
# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/', methods=['GET'])
def index():
    if current_user.is_anonymous:
        return render_template('index.html')
    return render_template('dashboard.html', user=current_user)

# Import a module / component using its blueprint handler variable (mod_auth)
from app.users.controllers import mod_users
from app.entries.controllers import mod_entries
from app.feedbacks.controllers import mod_feedbacks

# Register blueprint(s)
app.register_blueprint(mod_users)
app.register_blueprint(mod_entries)
app.register_blueprint(mod_feedbacks)

# Admin models
from app.users.models import User
from app.entries.models import Entry
from app.feedbacks.models import Feedback
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Entry, db.session))
admin.add_view(ModelView(Feedback, db.session))

# app.register_blueprint(xyz_module)
# ..
# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()