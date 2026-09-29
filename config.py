import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-change-me-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'instance' / 'umucopulse.db'}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB uploads
    UPLOAD_FOLDER = BASE_DIR / "app" / "static" / "uploads"
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "mp3", "mp4", "wav", "pdf"}
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@umucopulse.org")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Umuco123!")
    ITEMS_PER_PAGE = 20
