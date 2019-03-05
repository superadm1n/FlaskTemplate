from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from .forms import LoginForm, RegistrationForm
from .util import check_password, hash_password, required_roles
from datetime import datetime
from app import db, login_manager
from app.base import blueprint
from app.base.models import User, Role
from app.base.util import raise_flash_messages


@blueprint.route('/')
def index():
    return render_template('home.html')


#@blueprint.route('/<template>')
#@login_required
#def route_template(template):
#    return render_template(template + '.html')


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)

    if current_user.is_authenticated:
        return redirect(url_for('base_blueprint.index'))
    return render_template('login.html', login_form=login_form)


@blueprint.route('/login/user', methods=['POST'])
def log_user_in():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password(password, user.password) is True:
            login_user(user)
            flash('Login Successful, welcome {}.'.format(username))
            current_user.last_login = datetime.utcnow()
            db.session.commit()
            admin = User.query.filter_by(username='admin').first()
            if admin and check_password('admin', admin.password) is True:
                flash('WARNING! Default admin user exists on the system with the default password! please reset the password NOW!', 'danger')
            return redirect(url_for('base_blueprint.index'))
        flash('Invalid username or password!', 'danger')
        return redirect(url_for('base_blueprint.login'))
    else:
        return redirect('base_blueprint.login')


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('base_blueprint.index'))

    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data, password=hash_password(form.password.data))
            db.session.add(user)
            db.session.commit()
            flash('Registration Successful!', 'success')
            return redirect(url_for('base_blueprint.login'))
        else:
            raise_flash_messages(form)
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/page_404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/page_500.html'), 500
