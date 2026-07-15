from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
        app = Flask(__name__)

        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SECRET_KEY'] = 'change-this-to-something-random-later'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'instance', 'school.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)
        login_manager.init_app(app)
        login_manager.login_view = 'auth.login'

        from app.models import User

        @login_manager.user_loader
        def load_user(user_id):
                return User.query.get(int(user_id))
        return app