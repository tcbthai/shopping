from flask import redirect, render_template, url_for, flash, request
from . import auth
from forms import Register_Form, Login_Form, Password_Form
from app.models_sqldb import User
from app import db
from app.email import send_mail
from flask_login import login_user, login_required, logout_user, current_user


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = Register_Form()
    if form.validate_on_submit():
        if not form.check_email(form.email.data):
            user = User(nickname=form.nickname.data,
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            token = user.generate_token()
            send_mail(user.email, 'Confirm your account', 'auth/confirm', user=user, token=token)
            flash('A confirmation email has been sent to you by email.')
            return redirect(url_for('main.index'))
        flash("Email is already registered")
        return redirect(url_for('.register'))
    return render_template('auto_form.html', form=form, header='Register')


@auth.route('/confirm/<token>', methods=['GET', 'POST'])
def password_confirm(token):
    form = Password_Form()
    user_id = User.get_token_id(token)
    if not user_id:
        return render_template('custom_error.html')
    user = User.query.get(user_id)
    if not user or user.password_hash:
        return render_template('custom_error.html')
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('auto_form.html', form=form, header='Password')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = Login_Form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('invalid user or password')

    return render_template('auto_form.html', form=form, header='Login')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logged out')
    return redirect(url_for('main.index'))
