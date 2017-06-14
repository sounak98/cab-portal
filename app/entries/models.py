from app import db
from datetime import datetime

class Entry(db.Model):
    __tablename__ = 'entry'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_lon = db.Column(db.Float, nullable=False)
    start_lat = db.Column(db.Float, nullable=False)
    end_lon = db.Column(db.Float, nullable=False)
    end_lat = db.Column(db.Float, nullable=False)
    start = db.Column(db.String(100), nullable=False)
    end = db.Column(db.String(100), nullable=False)
    no_of_pass = db.Column(db.Integer, nullable=False)
    other_info = db.Column(db.String(500), nullable=True)
    done_or_not = db.Column(db.Boolean, nullable=False)
    time_of_travel = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, lon1=0, lat1=0, lon2=0, lat2=0, start='', end='', num=0, desc='', time=datetime.now(), user_id=0):
        self.start_lat = lat1
        self.start_lon = lon1
        self.end_lat = lat2
        self.end_lon = lon2
        self.start = start
        self.end = end
        self.no_of_pass = num
        self.other_info = desc
        self.time_of_travel = time
        self.user_id = user_id
        self.done_or_not = False

    def __repr__(self):
        return "<Entry %s>" % self.id
