from flask import request, render_template, Blueprint, json, redirect
from app import db,login_manager
from app.entries.models import Entry
from app.users.models import User
from flask_login import login_required, current_user
from datetime import datetime

mod_entries = Blueprint('entries', __name__)

@login_required
@mod_entries.route('/addEntry', methods = ['POST'])
def add_entry():
    try:
        if request.form['fromto'] == 'from':
            start_lat = 17.4447918
            start_lon = 78.34830979999992
            end_lat = request.form['latitude']
            end_lon = request.form['longitude']
            start = "IIIT, Gachibowli, Hyderabad, Telangana, India"
            end = request.form['address']
        else:
            end_lat = 17.4447918
            end_lon = 78.34830979999992
            start_lat = request.form['latitude']
            start_lon = request.form['longitude']
            end = "IIIT, Gachibowli, Hyderabad, Telangana, India"
            start = request.form['address']
        dateobj = datetime.strptime(request.form['datetime'] + ':00.0', "%Y-%m-%d %H:%M:%S.%f")
        entry = Entry(start_lon, start_lat, end_lon, end_lat, start, end, int(request.form['num']), request.form['info'], dateobj, current_user.id)
        db.session.add(entry)
        user = User.query.filter(User.id == current_user.id).first()
        user.entries.append(entry)
        db.session.commit()
        return json.jsonify(status=True)
    except Exception as e:
        print(e)
        return json.jsonify(status=False)

@login_required
@mod_entries.route('/history', methods = ['GET'])
def history():
    entries = User.query.filter(User.id == current_user.id).first().entries
    f_entries = []
    for entry in entries:
        if entry.done_or_not:
            f_entries.append(entry)
    return render_template('history.html', entries=f_entries, user=current_user)

@login_required
@mod_entries.route('/upcoming', methods = ['GET'])
def upcoming():
    entries = User.query.filter(User.id == current_user.id).first().entries
    f_entries = []
    for entry in entries:
        if not entry.done_or_not:
            f_entries.append(entry)
    return render_template('upcoming.html', entries=f_entries, user=current_user)

@login_required
@mod_entries.route('/matches', methods = ['GET'])
def matches():
    id = request.args.get('id')
    curr_entry = Entry.query.filter(Entry.id == id).first()
    entries = Entry.query.all()
    matches_data = []
    matches_user = []
    for entry in entries:
        if entry != curr_entry:
            if curr_entry.no_of_pass + entry.no_of_pass <= 4:
                if entry.start == curr_entry.start and entry.start == "IIIT, Gachibowli, Hyderabad, Telangana, India":
                    if entry.end_lon - curr_entry.end_lon <= 0.02:
                        if entry.end_lat - curr_entry.end_lon <= 0.02:
                            if (entry.time_of_travel - curr_entry.time_of_travel).seconds / 3600 <= 1:
                                matches_data.append(entry)
                                matches_user.append(User.query.filter(User.id == entry.user_id).first())
                elif entry.end == curr_entry.end and entry.end == "IIIT, Gachibowli, Hyderabad, Telangana, India":
                    if entry.start_lon - curr_entry.start_lon <= 0.02:
                        if entry.start_lat - curr_entry.start_lon <= 0.02:
                            if (entry.time_of_travel - curr_entry.time_of_travel).seconds / 3600 <= 1 or (curr_entry.time_of_travel - entry.time_of_travel) / 3600 <= 1:
                                matches_data.append(entry)
                                matches_user.append(User.query.filter(User.id == entry.user_id).first())
    return render_template('matches.html', matches=matches_data, user=current_user, matches_user=matches_user)

@login_required
@mod_entries.route('/confirmed', methods = ['POST'])
def confirmed():
    try:
        id = request.form['id']
        entry = Entry.query.filter(Entry.id == id).first()
        entry.done_or_not = True
        db.session.commit()
        return json.jsonify(status=True)
    except:
        return json.jsonify(status=False)