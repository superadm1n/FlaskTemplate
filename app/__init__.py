from app.config import ProductionConfig, TestConfig
from app.lib.scheduler import BackgroundScheduler
import datetime
from flask import Flask, g, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
import os

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
# Full directory path of the flask app
app_path = os.path.dirname(os.path.abspath(__file__))
# Final directory of flask app
app_dir = os.path.split(app_path)[-1]

from app.lib.passwords import hash_password
from app.models import User, Role
flask_app_obj = Flask(__name__, static_folder='static', template_folder='templates')
from app import routes  # Gives us the base application routes

scheduler = BackgroundScheduler()
scheduler.start()
from app.plugins.Plugin import Plugin

# creates a list of all of all the directories in the plugins folder which are
# the plugin blueprint and add them as blueprints
plugin_path = os.path.join(app_path, 'plugins')
plugins = [x for x in os.listdir(plugin_path)
           if os.path.isdir(os.path.join(plugin_path, x))
           and not x.startswith('__')]


@flask_app_obj.before_first_request
def initialize_database():
    db.create_all()


@flask_app_obj.teardown_request
def shutdown_session(exception=None):
    db.session.remove()


@flask_app_obj.before_request
def user_timeout():
    session.permanent = True
    flask_app_obj.permanent_session_lifetime = datetime.timedelta(minutes=60)
    session.modified = True
    g.user = current_user


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_plugins(app):
    # Container for holding route restrictions
    route_restriction_roles = []
    for module_name in plugins:
        module = import_module('{}.plugins.{}.routes'.format(app_dir, module_name))
        route_restriction_roles += module.plugin.access_roles
        app.register_blueprint(module.plugin)

    # return list of route restrictions for later processing
    return route_restriction_roles

def init_db():
    role = Role(name='admin')
    db.session.add(role)
    db.session.commit()

    user = User(username='admin', password='admin', email='admin@admin.com', roles=[role])
    db.session.add(user)
    db.session.commit()


def update_plugin_roles(route_restriction_roles):

    # takes all of the route restriction roles to the database if they dont exist.
    # this will make sure any plugin will have the proper roles so it doesnt throw a 500 error.
    with flask_app_obj.app_context():
        for role in route_restriction_roles:
            if not Role.query.filter_by(name=role).first():
                r = Role(name=role)
                db.session.add(r)
            db.session.commit()


def configure_logs(app):
    #basicConfig(filename='error.log', level=60)
    logger = getLogger()
    logger.addHandler(StreamHandler())


def create_app():
    app = flask_app_obj
    app.config.from_object(ProductionConfig)

    register_extensions(app)
    route_restrictions = register_plugins(app)
    update_plugin_roles(route_restrictions)
    configure_logs(app)

    return app


def create_test_app(db_file):
    app = flask_app_obj

    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_file)
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'Test_key'

    register_extensions(app)
    _ = register_plugins(app)
    #update_plugin_roles(route_restrictions)
    configure_logs(app)
    with app.app_context():
        import os
        if not os.path.isfile(db_file):
            db.create_all()
            init_db()

    return app
