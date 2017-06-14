from flask import request, render_template, Blueprint, json, redirect
from flask_login import login_required, current_user
from app.feedbacks.models import Feedback
from app import db

mod_feedbacks = Blueprint('feedbacks', __name__)

@login_required
@mod_feedbacks.route('/addFeedback', methods = ['POST'])
def add_feedback():
    try:
        feedback = Feedback(current_user.id, request.form['content'])
        db.session.add(feedback)
        db.session.commit()
        return json.jsonify(status=True)
    except:
        return json.jsonify(status=False)

@login_required
@mod_feedbacks.route('/feedback', methods = ['GET'])
def feedback():
    return render_template('feedback.html', user=current_user)