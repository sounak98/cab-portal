from flask import request, render_template, Blueprint, json, redirect, url_for
from app import db, login_manager
from app.users.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user

mod_users = Blueprint('users', __name__)

@mod_users.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            user = User(request.form['name'], request.form['phone'], generate_password_hash(request.form['password'], method='sha256'), request.form['email'])
            db.session.add(user)
            db.session.commit()
            return json.jsonify(status=True)
        except Exception as e:
            print(e)
            return json.jsonify(status=False)
    else:
        return render_template('register.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@mod_users.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        if not current_user.is_anonymous:
            return render_template('dashboard.html', user=current_user)
        return render_template('login.html')
    else:
        user = User.query.filter(User.email == request.form['email']).first()
        if user:
            if check_password_hash(user.password, request.form['password']):
                remember = False
                if request.form['remember'] == 'remember':
                    remember = True
                login_user(user, remember=remember)
                return redirect(url_for('users.dashboard'))
            else:
                return json.jsonify(status=False)
        else:
            return json.jsonify(status=False)

@mod_users.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@mod_users.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@login_required
@mod_users.route('/change-password', methods=['POST'])
def change_password():
    try:
        if check_password_hash(current_user.password, request.form['opw']):
            current_user.password = generate_password_hash(request.form['npw'], method='sha256')
            db.session.commit()
            return json.jsonify(status=True)
        else:
            return json.jsonify(status=False)
    except:
        return json.jsonify(status=False)

@login_required
@mod_users.route('/user-details', methods = ['GET'])
def user_details():
    return render_template('user.html', user=current_user)