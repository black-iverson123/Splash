from flask import render_template, url_for, redirect, flash, request, session
from app.extensions.forms import LoginForm, Signup, PasswordResetRequest, ResetPassword, updatePassword, searchForm
from app.extensions.models import User
from app.auth import bp
from app import db
from flask_login import login_user, login_required, logout_user, current_user
from app.extensions.email import send_mail
from app.extensions.token import confirm_token, generate_token
from datetime import datetime
from app.extensions.greeting import greeting

@bp.before_request
def before_request():
    """This function registers users last active"""
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    """View function that renders login page and redirects on authentication"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() or User.query.filter_by(email=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Bad login credentials!!!', 'danger')
            return redirect(url_for('auth.index'))
        login_user(user)
        session['name'] = current_user.username
        session['user_id'] = current_user.id
        return redirect(url_for('main.dashboard'))
    return render_template('auth/index.html', title='Log In ', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def signUp():
    """View funtion that handles redering of signup form and submission"""
    form = Signup()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        session['name'] = current_user.username
        session['user_id'] = current_user.id
        return redirect(url_for('auth.index'))
    return render_template('auth/signup.html', title='Sign Up', form=form)

@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """View function to log users out of the app and redirect to login page"""
    logout_user()
    flash("You have been logged out successfully!!!", 'warning')
    return redirect(url_for('auth.index'))

@bp.route("/confirm/<token>", methods=['GET', 'POST'])
def confirm_email(token):
    """View function for email address confirmation"""
    email = confirm_token(token)
    if email:
        user = db.session.query(User).filter(User.email == email).one_or_none()
        if user:
            user.confirmed = True
            user.confirmed_on = datetime.now()
            db.session.merge(user)
            db.session.commit()
            flash("You have confirmed your account. Thanks!", "success")
            return redirect(url_for("main.dashboard"))
    flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for("auth.resend_confirmation"))

@bp.route('/inactive', methods=['GET', 'POST'])
@login_required
def inactive():
    """View function that checks for user confirmation"""
    form = searchForm()
    if current_user.confirmed:
        return redirect(url_for("main.dashboard"))
    greet = greeting()
    return render_template("auth/inactive.html", title='Account inactive', greeting=greet, username=current_user.username, form=form)

@bp.route('/resend', methods=['GET', 'POST'])
@login_required
def resend_confirmation():
    """View function that checks for user confirmation and resends email if not"""
    if current_user.confirmed:
        flash("Your account has already been confirmed!!!", 'success')
        return redirect(url_for('main.dashboard'))
    token = generate_token(current_user.email)
    html = render_template('email/confirm_email.html', token=token)
    subject = "Please confirm your email"
    send_mail(current_user.email, subject, html)
    flash(f"An email has been sent to {current_user.email}!!!.", 'info')
    return redirect(url_for('auth.inactive', username=current_user.username))

@bp.route('/reset_password', methods=['GET', 'POST'])
def password_reset():
    """View function that sends email based on reset password request"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    greet = greeting()
    form = PasswordResetRequest()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_password_reset_token()
            html = render_template('email/password_reset.html', user=user, token=token)
            subject = "[Splash] Reset your Password"
            send_mail(user.email, subject, html)
        flash('Check your email for instructions to reset your password!!!', 'info')
        return redirect(url_for('auth.index'))
    return render_template('auth/password_reset.html', title='Reset Password', form=form, greeting=greet)

@bp.route('/password_reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """View function that crosschecks token recieved from user and validates before
        allowing form rendering
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    user = User.verify_password_reset_token(token)
    if not user:
        return redirect(url_for('auth.index'))
    form = ResetPassword()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset!!!', 'warning')
        return redirect(url_for('auth.index'))
    return render_template('auth/reset_password.html', form=form)

@login_required
@bp.route('/password_update', methods=['GET', 'POST'])
def updatePwd():
    """View function to update or change password in app"""
    form = updatePassword()
    if request.method == 'POST':
        email = request.form.get('email')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        user = User.query.filter_by(email=email).first()
        if user.id == current_user.id:
            if not user.check_password(old_password):
                flash('Old password is wrong, please try again!', 'warning')
            elif new_password != confirm_password:
                flash('Passwords do not match, please try again!', 'warning')
            elif len(new_password) < 7:
                flash('Password must be at least 7 characters long!', 'warning')
            else:
                user.set_password(new_password)
                db.session.commit()
                flash('Password has been updated successfully!', 'success')
                return redirect(url_for('main.dashboard'))
    return render_template('auth/password_update.html', user=current_user, form=form)