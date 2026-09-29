from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

ROLE_CHOICES = [
    ("Cultural practitioner", "Cultural practitioner"),
    ("Artist", "Artist"),
    ("Dancer", "Dancer"),
    ("Musician", "Musician"),
    ("Poet", "Poet"),
    ("Researcher", "Researcher"),
    ("Educator", "Educator"),
    ("Student", "Student"),
    ("Diaspora member", "Diaspora member"),
    ("Institution", "Institution"),
    ("Supporter", "Supporter"),
    ("Other", "Other"),
]

STORY_CATEGORY_CHOICES = [
    ("poetry", "Poetry"),
    ("dance", "Dance & Movement"),
    ("music", "Stories & Song"),
    ("oral_history", "Oral History"),
    ("craft", "Craft & Heritage"),
]

STORY_TYPE_CHOICES = [
    ("written", "Written Story"),
    ("audio", "Audio Recording"),
    ("video", "Video Recording"),
]


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    role = SelectField("Role", choices=ROLE_CHOICES, validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=10, max=2000)])


class NewsletterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=120)])


class StorySubmissionForm(FlaskForm):
    title = StringField("Story Title", validators=[DataRequired(), Length(min=5, max=200)])
    category = SelectField("Category", choices=STORY_CATEGORY_CHOICES, validators=[DataRequired()])
    story_type = SelectField("Format", choices=STORY_TYPE_CHOICES, validators=[DataRequired()])
    content = TextAreaField(
        "Your Story",
        validators=[DataRequired(), Length(min=50, max=5000)],
        render_kw={"placeholder": "Share your cultural story, poem, or oral history..."},
    )
    consent = BooleanField(
        "I confirm that I have permission to share this story and any attached media, and I consent to UmucoPulse reviewing it for possible publication.",
        validators=[DataRequired(message="Consent is required before submission.")],
    )
    consent_level = SelectField(
        "Who may see this after review",
        choices=[
            ("public", "Public"),
            ("members", "Members only"),
            ("private", "Private archive"),
        ],
        validators=[DataRequired()],
    )
    credit_role = SelectField(
        "Credit",
        choices=[
            ("shared_by", "Shared by"),
            ("original", "Original practitioner"),
            ("community", "Community"),
            ("source", "Source"),
        ],
        validators=[DataRequired()],
    )
    credit_name = StringField("Credit name", validators=[Optional(), Length(max=120)])


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])


class RegisterForm(FlaskForm):
    name = StringField("Full name", validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=128)])
    confirm = PasswordField(
        "Confirm password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )


class MentorshipForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    request_type = SelectField(
        "I want to",
        choices=[("request", "Request mentorship"), ("offer", "Offer mentorship")],
        validators=[DataRequired()],
    )
    focus_area = SelectField(
        "Focus area",
        choices=[
            ("storytelling", "Storytelling"),
            ("dance", "Dance"),
            ("music", "Music"),
            ("archive", "Digital archiving"),
            ("education", "Cultural education"),
        ],
        validators=[DataRequired()],
    )
    details = TextAreaField("Details", validators=[DataRequired(), Length(min=20, max=2000)])


class ProjectFilterForm(FlaskForm):
    category = SelectField(
        "Filter by category",
        choices=[
            ("all", "All Projects"),
            ("education", "Education & Workshops"),
            ("archive", "Digital Archive"),
            ("performance", "Performances & Events"),
        ],
        validators=[Optional()],
    )
