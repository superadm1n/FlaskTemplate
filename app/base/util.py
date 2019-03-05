from flask import redirect, url_for, flash
from flask_login import current_user
from app import bcrypt
from functools import wraps
from datetime import datetime
from dateutil import tz
import random
import string

def random_string(length=8):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))


def hash_password(pw):
    return bcrypt.generate_password_hash(pw).decode('utf-8')


def check_password(pw, hashed_pw):
    return bcrypt.check_password_hash(hashed_pw.encode('utf-8'), pw.encode('utf-8'))


def required_roles(*roles):
    '''Custom function for checking if a user has the required rolls to access a resource.
    :param roles:
    :return:
    '''

    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                if bool(set(roles) & {role.name for role in current_user.roles}) is False:
                    return redirect(url_for('base_blueprint.route_default'))
            except AttributeError:
                return redirect(url_for('base_blueprint.route_default'))
            return f(*args, **kwargs)

        return wrapped

    return wrapper


def convert_time(time, timeZone='America/Central'):

    '''
    Method to easily convert time zone
    :param time:
    :param timeZone:
    :return:
    '''
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(timeZone)

    utc = datetime.strptime(time.split('.')[0], '%Y-%m-%d %H:%M:%S')

    # Tell the datetime object that it's in UTC time zone since
    # datetime objects are 'naive' by default
    utc = utc.replace(tzinfo=from_zone)

    # Convert time zone
    convertedTime = utc.astimezone(to_zone)

    return convertedTime


def raise_flash_messages(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(error, 'danger')