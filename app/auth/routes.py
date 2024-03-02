from app.auth.forms import LoginForm, RegisterationForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa
from app import db
from app.models import User
from app.auth import bp
from urllib.parse import urlsplit


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        query = sa.select(User).where(User.username==form.username.data)
        user = db.session.scalar(query)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
        else:
            flash("Invalid user or password")
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # flash("Congratulations on successful registeration")
        print("Congratulations on successful registeration")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title="Register", form=form)
