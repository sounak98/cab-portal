from app import db

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)

    def __init__(self, user_id=0, content=''):
        self.user_id = user_id
        self.content = content

    def __repr__(self):
        return "<Feedback %s>" % self.id