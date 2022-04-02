"""
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '7d695dda8bd89b7e825b0388822b7471'
bcrypt=Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_site.db'
db = SQLAlchemy(app)

class User(db.Model):
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
    tracker_id = db.Column(db.Integer, db.ForeignKey("tracker.tracker_id"), nullable=False)

    def __init__(self, when, value, tracer_id):
        self.when = when
        self.value = value


@app.route("/", methods=["POST", "GET"])
def home():
    form=LoginForm()
    if request.method == 'POST':
        return render_template('tracker.html')
    return render_template('login.html',form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created ! You are now able to login','success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route("/tracker", methods=["GET", "POST"])
def tracker():
    if request.method == 'POST':
        name = request.form['tname']
        description = request.form['desc']
        type = request.form.get("data_type")
        settings = request.form["set"]
        print(type)
        if type == 'Numeric':
            type = str(1)
        elif type == 'Mutiple':
            type = str(2)
        else:
            type = str(3)
        print(name, description, type, settings)
        new_tracker = Tracker(name, description, type, settings)
        db.session.add(new_tracker)
        db.session.commit()
    return render_template('add_tracker.html')
"""
from activitytrackiing import app
if __name__ == '__main__':
    app.run(debug=True)
