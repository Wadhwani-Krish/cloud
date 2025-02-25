import functools
import random
import pymysql
import pyotp
import smtplib
import os

from email.message import EmailMessage
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from modelEarth_login import oauth

from modelEarth_login.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not email or len(email) < 5 or len(email) > 50:
            error = 'Invalid email length'
        if not username or len(username) < 3 or len(username) > 30:
            error = 'Invalid username length.'
        elif not password or len(password) < 8:
            error = 'Password must be at least 8 characters long.'

        if error is None:
            try:

                with db.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO user (email, username, password) VALUES (%s, %s, %s)",
                        (email, username, generate_password_hash(password)),
                    )
                db.commit()
            except pymysql.err.IntegrityError:
                error = f"User {username} or email {email} is already registered."
            else:
                return redirect(url_for("auth.login_step", email=email))

        flash(error)

    return render_template('auth/register.html')


@bp.route("/google_login")
def google_login():

    google = oauth.create_client("google")
    redirect_uri = url_for("auth.google_callback", _external=True)
    return google.authorize_redirect(redirect_uri)


@bp.route("/google/callback")
def google_callback():
    """Handle Google OAuth callback and log in user"""
    google = oauth.create_client("google")
    token = google.authorize_access_token()
    user_info = google.get("https://www.googleapis.com/oauth2/v3/userinfo").json()

    if not user_info:
        flash("Google login failed!", "danger")
        return redirect(url_for("auth.login_step"))

    email = user_info["email"]
    name = user_info.get("name", email.split("@")[0])  # Use email as fallback for username

    db = get_db()

    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            # If user doesn't exist, register them
            cursor.execute(
                "INSERT INTO user (email, username, password, totp_secret, is_google) VALUES (%s, %s, %s, %s, %s)",
                (email, name, None, None, True),
            )
            db.commit()
            cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
            user = cursor.fetchone()

    session["user_id"] = user["id"]

    flash("Logged in successfully with Google!", "success")
    if user.get("is_admin"):
        return redirect(url_for("admin.admin_index"))  # Redirect admin users
    return redirect(url_for("index"))


@bp.route("/login_step", methods=["GET", "POST"])
def login_step():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        error = None

        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            user = cursor.fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # Store email in session for next step
            session["email"] = user["email"]
            session["username"] = user["username"]
            session['user_id'] = user['id']
            return redirect(url_for("auth.login"))  # Go to OTP verification page

        flash(error)

    return render_template("auth/login_step.html")  # First step login template

@bp.route("/login", methods=["GET", "POST"])
def login():
    email = session.get('email')
    username = session.get("username")

    if not email:
        flash("Invalid session. Please log in again.")
        return redirect(url_for("auth.login_step"))

    if request.method == 'GET':

        otp_secret = pyotp.random_base32()
        print(otp_secret)

        session['otp_secret'] = otp_secret
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(os.environ.get('email_id'), os.environ.get('email_pass'))
        msg = EmailMessage()
        msg['Subject'] = 'OTP Verification'
        msg['From'] = 'krishwadhwani.work@gmail.com'
        msg['To'] = email
        msg.set_content("Your OTP is: " + otp_secret)
        server.send_message(msg)
        print("Email send.")



        return render_template('auth/login.html', email=email)

    if request.method == 'POST':
        otp_secret = session.get('otp_secret')
        otp = request.form['otp']

        user_id = session.get('user_id')


        db = get_db()
        error = None
        if not otp_secret == str(otp):
            error = 'Invalid one-time password.'

        if error is None:
            session['user_id'] = user_id
            session.pop("email", None)
            session.pop("username", None)

            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    db = get_db()
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute('SELECT * FROM user WHERE id = %s', (user_id,))
            g.user = cursor.fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or not g.user.get('is_admin'):
            flash('Admin access required.', 'error')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
