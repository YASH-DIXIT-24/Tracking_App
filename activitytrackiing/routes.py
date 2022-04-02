from flask import render_template, url_for, flash, redirect, request
import datetime as DT
from activitytrackiing.forms import RegistrationForm, LoginForm
from activitytrackiing.models import User, Tracker, TrackerLogs
from activitytrackiing import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/", methods=["POST", "GET"])
def home():
    return redirect(url_for('login'))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, str(form.password.data)):
            login_user(user, remember=form.remember.data)
            flash('Login Successful', 'success')
            return redirect(url_for('tracker'))
        else:
            flash('Login Unsuccessful, Please check your email and Password', 'danger')
    return render_template('login.html', form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    print(form.username.data)
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created ! You are now able to login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/add_tracker", methods=["GET", "POST"])
@login_required
def add_tracker():
    if request.method == 'POST':
        name = request.form['tname']
        description = request.form['desc']
        track_type = request.form["type"]
        settings = request.form["set"]
        print(track_type)
        if track_type == 'Numerical':
            track_type = str(1)
        else:
            track_type = str(2)

        new_tracker = Tracker(name, description, track_type, settings)
        user = User.query.get(current_user.id)
        user.trackers.append(new_tracker)
        db.session.commit()
        return redirect(url_for('tracker'))
    return render_template('add_tracker.html')


@app.route("/tracker_log/<int:tracker_id>", methods=["POST", "GET"])
def tracker_log(tracker_id):
    track = Tracker.query.get(tracker_id)
    if request.method == 'POST':
        when = request.form.get('log_time')
        date_processing = when.replace('T', '-').replace(':', '-').split('-')
        date_processing = [int(v) for v in date_processing]
        date_out = DT.datetime(*date_processing)
        value = request.form.get('value')
        notes = request.form.get('notes')
        new_log = TrackerLogs(date_out, value, notes)
        track.logs.append(new_log)
        db.session.commit()
        return redirect(url_for('tracker'))
    return render_template('tracker_log.html', tracker=track)


@app.route("/tracker")
def tracker():
    trackers = Tracker.query.all()
    a = []
    lat_date = dict()
    for track in trackers:
        a = []
        if len(track.logs) != 0:
            for log in track.logs:
                a.append(log.when)
            latest = max(a)
            lat_date[track.tracker_name] = latest
    return render_template('tracker.html', trackers=trackers, lat_date=lat_date)


@app.route("/track_info/<int:tracker_id>")
def track_info(tracker_id):
    trackers = Tracker.query.get(tracker_id)
    logs = trackers.logs
    data = {'': ''}
    for log in logs:
        if log.value in data:
            data[log.value] += 1
        else:
            data[log.value] = 1
    return render_template('track_info.html', trackers=trackers, data=data)


@app.route("/update_tracker/<int:tracker_id>", methods=["POST", "GET"])
@login_required
def update_tracker(tracker_id):
    track = Tracker.query.get(tracker_id)

    if request.method == 'POST':
        name = request.form['tname']
        if len(name):
            track.tracker_name = name
        if len(request.form['desc']):
            track.tracker_desc = request.form['desc']
        track_type = request.form["type"]
        if len(request.form["set"]):
            track.settings = request.form["set"]
        if track_type == 'Numerical':
            track_type = str(1)
        else:
            track_type = str(2)
        if len(track_type):
            track.tracker_type = track_type
        db.session.commit()
        return redirect(url_for('tracker'))
    return render_template('update_tracker.html')


@app.route("/delete_tracker/<int:tracker_id>")
def delete_tracker(tracker_id):
    track = Tracker.query.get(tracker_id)
    db.session.delete(track)
    db.session.commit()
    return redirect(url_for('tracker'))


@app.route("/delete_log/<int:log_id>/<int:tracker_id>")
def delete_log(log_id, tracker_id):
    log=TrackerLogs.query.get(log_id)
    db.session.delete(log)
    db.session.commit()
    return redirect(url_for('tracker'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
