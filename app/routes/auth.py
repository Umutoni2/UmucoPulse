from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import db
from app.forms import LoginForm, RegisterForm
from app.models import CulturalProfile, User

auth_bp = Blueprint("auth", __name__)


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not current_user.is_admin:
            flash("Administrator access is required.", "error")
            return redirect(url_for("main.index"))
        return view(*args, **kwargs)

    return wrapped


def contributor_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if current_user.is_admin:
            return redirect(url_for("admin.dashboard"))
        return view(*args, **kwargs)

    return wrapped


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "error")
            return render_template("auth/register.html", form=form)

        user = User(name=form.name.data.strip(), email=email, role="contributor")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        db.session.add(
            CulturalProfile(
                user_id=user.id,
                display_name=user.name,
                area="oral",
                is_public=False,
                is_demo=False,
                profile_kind="individual",
            )
        )
        db.session.commit()
        login_user(user)
        flash("Welcome to UmucoPulse. Start by building your cultural profile.", "success")
        return redirect(url_for("main.profile"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user and user.is_active_account and user.check_password(form.password.data):
            login_user(user)
            flash(f"Welcome back, {user.name}.", "success")
            next_page = request.args.get("next")
            if user.is_admin:
                return redirect(next_page or url_for("admin.dashboard"))
            return redirect(next_page or url_for("main.dashboard"))
        flash("Incorrect email or password.", "error")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))
