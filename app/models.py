from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


def utcnow():
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default="contributor", index=True)
    is_active_account = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utcnow)

    submissions = db.relationship("StorySubmission", backref="author", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == "admin"


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    inbox_status = db.Column(db.String(20), default="unread", index=True)
    source = db.Column(db.String(40), default="contact")
    subject = db.Column(db.String(200), default="")
    created_at = db.Column(db.DateTime, default=utcnow, index=True)


class NewsletterSubscriber(db.Model):
    __tablename__ = "newsletter_subscribers"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utcnow)


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    image = db.Column(db.String(200), default="assets/workshops.svg")
    area = db.Column(db.String(40), default="")
    status = db.Column(db.String(20), default="active", index=True)
    start_date = db.Column(db.String(40), default="")
    end_date = db.Column(db.String(40), default="")
    is_public = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utcnow)


class Voice(db.Model):
    __tablename__ = "voices"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    contributor = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    quote = db.Column(db.String(300))
    image = db.Column(db.String(200), default="assets/voices.svg")
    credit_role = db.Column(db.String(40), default="shared_by")
    credit_name = db.Column(db.String(120), default="")
    consent_level = db.Column(db.String(20), default="public")
    is_featured = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default="published", index=True)
    moderation_status = db.Column(db.String(20), default="active", index=True)
    created_at = db.Column(db.DateTime, default=utcnow)


class StorySubmission(db.Model):
    __tablename__ = "story_submissions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    story_type = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    consent = db.Column(db.Boolean, default=False)
    consent_level = db.Column(db.String(20), default="public")
    credit_role = db.Column(db.String(40), default="shared_by")
    credit_name = db.Column(db.String(120), default="")
    status = db.Column(db.String(20), default="pending", index=True)
    admin_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=utcnow, index=True)
    published_at = db.Column(db.DateTime)


class MentorshipRequest(db.Model):
    __tablename__ = "mentorship_requests"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    request_type = db.Column(db.String(20), nullable=False)
    focus_area = db.Column(db.String(80), nullable=False)
    details = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="open", index=True)
    created_at = db.Column(db.DateTime, default=utcnow)


class FocusMetric(db.Model):
    __tablename__ = "focus_metrics"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    label = db.Column(db.String(200), nullable=False)
    value = db.Column(db.Integer, default=0)
    target = db.Column(db.Integer, default=100)
    icon = db.Column(db.String(50), default="archive")


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    level = db.Column(db.String(50))
    rating = db.Column(db.Integer, default=3)
    sort_order = db.Column(db.Integer, default=0)


class CulturalProfile(db.Model):
    __tablename__ = "cultural_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    display_name = db.Column(db.String(120), nullable=False)
    area = db.Column(db.String(40), nullable=False, index=True)
    role = db.Column(db.String(120), default="")
    location = db.Column(db.String(120), default="")
    languages = db.Column(db.String(200), default="")
    bio = db.Column(db.Text, default="")
    background = db.Column(db.Text, default="")
    skills = db.Column(db.Text, default="")
    available = db.Column(db.Text, default="")
    profile_kind = db.Column(db.String(40), default="individual", index=True)
    website = db.Column(db.String(300), default="")
    photo = db.Column(db.String(200), default="")
    community_note = db.Column(db.Text, default="")
    is_public = db.Column(db.Boolean, default=False)
    curated = db.Column(db.Boolean, default=False)
    is_demo = db.Column(db.Boolean, default=False)
    location_key = db.Column(db.String(40), default="unlisted", index=True)
    source_info = db.Column(db.String(300), default="")
    social_link = db.Column(db.String(300), default="")
    moderation_status = db.Column(db.String(20), default="active", index=True)

    portfolio = db.relationship("PortfolioItem", backref="profile", lazy=True, cascade="all, delete-orphan")

    def available_list(self):
        return [part for part in (self.available or "").split("|") if part]

    def initials(self):
        parts = (self.display_name or "?").split()
        return "".join(p[0] for p in parts[:2]).upper()

    def kind_key(self):
        return self.profile_kind or "individual"

    def practices_list(self):
        raw = (self.skills or "").replace("·", ",").replace("|", ",")
        return [part.strip() for part in raw.split(",") if part.strip()]


class PortfolioItem(db.Model):
    __tablename__ = "portfolio_items"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("cultural_profiles.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    item_type = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, default="")
    context = db.Column(db.Text, default="")
    link = db.Column(db.String(300), default="")
    date_label = db.Column(db.String(40), default="")
    media_name = db.Column(db.String(200), default="")


class Follow(db.Model):
    __tablename__ = "follows"

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey("cultural_profiles.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow)


class CollaborationRequest(db.Model):
    __tablename__ = "collaboration_requests"

    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    from_name = db.Column(db.String(120), nullable=False)
    to_profile_id = db.Column(db.Integer, db.ForeignKey("cultural_profiles.id"), nullable=False)
    request_type = db.Column(db.String(80), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="Pending")
    created_at = db.Column(db.DateTime, default=utcnow)


class Opportunity(db.Model):
    __tablename__ = "opportunities"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(120), default="")
    description = db.Column(db.Text, nullable=False)
    is_demo = db.Column(db.Boolean, default=True)


class CulturalEvent(db.Model):
    __tablename__ = "cultural_events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    event_type = db.Column(db.String(40), nullable=False, index=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("cultural_profiles.id"), nullable=True)
    location = db.Column(db.String(120), default="")
    location_key = db.Column(db.String(40), default="unlisted")
    date_label = db.Column(db.String(80), default="")
    description = db.Column(db.Text, default="")
    is_demo = db.Column(db.Boolean, default=True)
    is_public = db.Column(db.Boolean, default=True)


class Favourite(db.Model):
    __tablename__ = "favourites"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    item_type = db.Column(db.String(40), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow)


class ContentReport(db.Model):
    __tablename__ = "content_reports"

    id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.String(40), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(80), nullable=False)
    details = db.Column(db.Text, default="")
    reporter = db.Column(db.String(120), default="")
    status = db.Column(db.String(40), default="new", index=True)
    decision = db.Column(db.String(40), default="")
    decision_reason = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=utcnow)
    updated_at = db.Column(db.DateTime, default=utcnow)


class LibraryItem(db.Model):
    __tablename__ = "library_items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content_type = db.Column(db.String(80), nullable=False, index=True)
    area = db.Column(db.String(40), default="", index=True)
    short_description = db.Column(db.Text, default="")
    full_description = db.Column(db.Text, default="")
    author = db.Column(db.String(160), default="")
    original_source = db.Column(db.String(300), default="")
    community = db.Column(db.String(160), default="")
    publication_date = db.Column(db.String(40), default="")
    location = db.Column(db.String(120), default="")
    language = db.Column(db.String(80), default="")
    cover_name = db.Column(db.String(200), default="")
    file_name = db.Column(db.String(200), default="")
    external_link = db.Column(db.String(400), default="")
    keywords = db.Column(db.String(300), default="")
    cultural_context = db.Column(db.Text, default="")
    credits = db.Column(db.String(300), default="")
    rights = db.Column(db.Text, default="")
    consent = db.Column(db.Boolean, default=False)
    visibility = db.Column(db.String(20), default="draft", index=True)
    status = db.Column(db.String(20), default="draft", index=True)
    created_at = db.Column(db.DateTime, default=utcnow)


class ActivityLog(db.Model):
    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(80), nullable=False)
    item = db.Column(db.String(200), default="")
    admin_name = db.Column(db.String(120), default="")
    created_at = db.Column(db.DateTime, default=utcnow, index=True)


class SiteSetting(db.Model):
    __tablename__ = "site_settings"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True, nullable=False)
    value = db.Column(db.String(300), default="")

