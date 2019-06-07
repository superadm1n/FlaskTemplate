from app import db, login_manager
from flask_login import UserMixin
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(120))
    last_login = Column(db.DateTime, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)

    logs = db.relationship("UserLog")
    roles = db.relationship('Role', secondary='user_roles')
    groups = db.relationship('Group', secondary='group_users')

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    def has_role(self, *args):
        '''Allows Jinja to check to see if a current user has a particular role

        :param args: roles
        :return:
        '''
        # Gets all of the associated roles a user has access to via their assigned groups
        group_associated_roles = []
        for group in self.groups:
            for role in group.roles:
                group_associated_roles.append(role)

        # List containing all of the roles a user is associated with
        all_associated_roles = group_associated_roles + self.roles

        return bool(set(args) & {role.name for role in all_associated_roles})


# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return 'Role({}, {})'.format(self.id, self.name)
    

# Define the Group data-model
class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    roles = db.relationship('Role', secondary='group_roles')
    users = db.relationship('User', secondary='group_users')

    def __repr__(self):
        return 'Group({}, {})'.format(self.id, self.name)


class UserLog(db.Model):
    __tablename__ = 'user_log'
    id = db.Column(db.Integer(), primary_key=True)
    message = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    user = db.Column(Integer, db.ForeignKey('user.id'))


# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# Define the GroupRoles association table
class GroupRoles(db.Model):
    __tablename__ = 'group_roles'
    id = db.Column(db.Integer(), primary_key=True)
    group_id = db.Column(db.Integer(), db.ForeignKey('group.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# Define the GroupUsers association table
class GroupUsers(db.Model):
    __tablename__ = 'group_users'
    id = db.Column(db.Integer(), primary_key=True)
    group_id = db.Column(db.Integer(), db.ForeignKey('group.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


#@login_manager.request_loader
#def request_loader(request):
#    username = request.form.get('username')
#    user = User.query.filter_by(username=username).first()
#    return user if user else None
