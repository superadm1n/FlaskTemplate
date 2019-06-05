'''

'''

from unittest import TestCase
import os
from app import db, create_test_app
from app.models import User, Role, UserRoles
from app.lib.passwords import hash_password
from flask import url_for, get_flashed_messages


class BaseCase(TestCase):

    '''
    All tests should ultimately inherit from this BaseCase
    test case to ensure proper setup and teardown of the test case
    '''
    dbpath = os.path.dirname(os.path.abspath(__file__)) + '/unittest.db'
    with open(dbpath, 'w') as f:
        pass
    app = create_test_app(dbpath)

    def setUp(self):
        with self.app.test_request_context():
            db.create_all()

    def tearDown(self):
        if os.path.isfile(self.dbpath):
            os.remove(self.dbpath)

    def _add_to_db(self, obj):
        with self.app.test_request_context():
            db.session.add(obj)
            db.session.commit()

    def add_role(self, name):
        role = Role(name=name)
        self._add_to_db(role)

    def add_std_user(self, username, password, email):
        user = User(username=username, password=password, email=email, image_file='')
        self._add_to_db(user)

    def add_admin_user(self, username, password, email):
        with self.app.test_request_context():
            role_existance = Role.query.filter_by(name='admin').first()

        if not role_existance:
            self.add_role('admin')

            with self.app.test_request_context():
                role_existance = Role.query.filter_by(name='admin').first()
        user = User(username=username, password=password, email=email, image_file='')
        self._add_to_db(user)
        with self.app.test_request_context():
            user = User.query.filter_by(username=username).first()

        userRole = UserRoles(user_id=user.id, role_id=role_existance.id)
        self._add_to_db(userRole)

    def login_as_user_id(self, user_id):
        '''Makes the session authenticated as the first user in the db (admin)'''
        with self.app.test_client() as tester:
            with tester.session_transaction() as sess:
                sess['user_id'] = str(user_id)
                sess['_fresh'] = True  # https://flask-login.readthedocs.org/en/latest/#fresh-logins
        return tester

    def generate_url(self, blueprint, **kwargs):
        '''Allows the user to generate urls using url_for'''
        with self.app.test_request_context():
            if not kwargs:
                url = url_for(blueprint)
                return url
            else:
                url = url_for(blueprint, **kwargs)
                return url

    def anonymous_user(self):
        with self.app.test_client() as tester:
            return tester

    def get_flashed_messages(self, tester, type='danger'):
        with tester.session_transaction() as session:
            return dict(session['_flashes']).get(type)

    def add_base_users(self):
        self.add_role('admin')
        self.add_std_user('stduser', hash_password('pass'), 'stduser@stduser.com')
        self.add_admin_user('adminuser', hash_password('pass'), 'adminuser@admin.com')
        with self.app.test_request_context():
            self.std_user = User.query.filter_by(username='stduser').first()
            self.admin_user = User.query.filter_by(username='adminuser').first()


class BaseTest(BaseCase):

    def setUp(self):
        super().setUp()
        self.add_base_users()