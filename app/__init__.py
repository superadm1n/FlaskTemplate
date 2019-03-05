from app.config import ProductionConfig, TestConfig
from flask import Flask, g, session
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler

import os
import datetime

db = SQLAlchemy()
login_manager = LoginManager()
dir_path = os.path.dirname(os.path.realpath(__file__))
bcrypt = Bcrypt()

from app.scheduler import start_schedule
from app.base.models import User, Role
from app.base.util import hash_password

#scheduler = start_schedule()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('base',):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def create_admin_user():

    role = Role()
    role.name = 'Admin'
    db.session.add(role)
    db.session.commit()

    user = User()
    user.username = 'admin'
    user.password = hash_password('admin')
    user.email = 'admin@admin.com'
    user.roles = [role,]

    db.session.add(user)
    db.session.commit()

def create_dev_roll():

    role = Role()
    role.name = 'Developer'
    db.session.add(role)
    db.session.commit()


def init_db():
    create_admin_user()
    create_dev_roll()


def configure_database(app, testing=False):

    @app.before_first_request
    def initialize_database():
        db.create_all()



    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def configure_logs(app):
    basicConfig(filename='error.log', level=DEBUG)
    logger = getLogger()
    logger.addHandler(StreamHandler())


def configure_user_timeout(app):

    '''
    Sets the user timeout of the app to 20 minutes. The 'user_timeout' function
    will run whenever the user makes a request to the server.
    '''

    @app.before_request
    def user_timeout():
        session.permanent = True
        app.permanent_session_lifetime = datetime.timedelta(minutes=60)
        session.modified = True
        g.user = current_user


def create_app():
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(ProductionConfig)

    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    configure_logs(app)

    configure_user_timeout(app)
    start_schedule(app)
    return app


def create_test_app(db_file):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(TestConfig)

    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    configure_logs(app)
    configure_user_timeout(app)
    with app.app_context():
        import os
        if not os.path.isfile(db_file):
            db.create_all()
            init_db()

    return app