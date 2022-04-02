from activitytrackiing import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    trackers = db.relationship('Tracker', backref='tracker', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Tracker(db.Model):
    tracker_id = db.Column(db.Integer, primary_key=True)
    tracker_name = db.Column(db.String(20), nullable=False)
    tracker_desc = db.Column(db.String(100))
    tracker_type = db.Column(db.Enum('1', '2', '3'), nullable=False)
    settings = db.Column(db.String(40), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    logs = db.relationship('TrackerLogs', backref='user', lazy=True)

    def __init__(self, tracker_name, tracker_desc, tracker_type, settings):
        self.tracker_name = tracker_name
        self.tracker_desc = tracker_desc
        self.tracker_type = tracker_type
        self.settings = settings


class TrackerLogs(db.Model):
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    when = db.Column(db.DateTime)
    value = db.Column(db.String(20))
    notes = db.Column(db.String(60))
    tracker_id = db.Column(db.Integer, db.ForeignKey("tracker.tracker_id"))

    def __init__(self, when, value, notes):
        self.when = when
        self.value = value
        self.notes = notes
