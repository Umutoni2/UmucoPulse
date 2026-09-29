from flask import Flask, session
from pathlib import Path

from app.extensions import csrf, db, login_manager
from app.i18n import TRANSLATIONS, get_ui
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.before_request
    def localize_login_message():
        lang = session.get("lang", "en")
        login_manager.login_message = get_ui(lang).get("login_needed", "Please log in to continue.")

    from app.forms import NewsletterForm
    from datetime import datetime, timezone

    @app.context_processor
    def inject_globals():
        lang = session.get("lang", "en")
        return {
            "newsletter_form": NewsletterForm(),
            "now": lambda: datetime.now(timezone.utc),
            "t": TRANSLATIONS.get(lang, TRANSLATIONS["en"]),
            "current_lang": lang,
        }

    with app.app_context():
        db.create_all()
        from app.seed import seed_database

        seed_database()

    return app
