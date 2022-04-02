from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '7d695dda8bd89b7e825b0388822b7471'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view='login'
from activitytrackiing import routes
