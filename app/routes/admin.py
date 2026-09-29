from datetime import datetime, timedelta
from pathlib import Path

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename

from app.culture import LIBRARY_TYPES, LIBRARY_VISIBILITY, PROFILE_KINDS, PROFILE_STATUSES, PROJECT_STATUSES, REPORT_REASONS
from app.extensions import db
from app.i18n import get_areas
from app.models import (
    ActivityLog,
    CollaborationRequest,
    ContactMessage,
    ContentReport,
    CulturalProfile,
    Follow,
    LibraryItem,
    PortfolioItem,
    Project,
    SiteSetting,
    StorySubmission,
    Voice,
    utcnow,
)
from app.routes.auth import admin_required

admin_bp = Blueprint("admin", __name__)

LIBRARY_TABS = ["All", "Documentary", "Booklet", "Magazine", "Audio", "Video", "Other"]


@admin_bp.context_processor
def inject_admin_chrome():
    if not (current_user.is_authenticated and getattr(current_user, "is_admin", False)):
        return {}
    pending = StorySubmission.query.filter_by(status="pending").count()
    reports = ContentReport.query.filter(ContentReport.status.in_(["new", "open", "under_review"])).count()
    unread = ContactMessage.query.filter_by(is_read=False).count()
    return {
        "pending_reviews": pending,
        "nav_alerts": pending + reports + unread,
    }


def _day_keys(days=7):
    today = datetime.utcnow().date()
    return [today - timedelta(days=days - 1 - i) for i in range(days)]


def _count_by_day(model, days=7):
    keys = _day_keys(days)
    buckets = {k.isoformat(): 0 for k in keys}
    start = datetime.combine(keys[0], datetime.min.time())
    try:
        rows = model.query.filter(model.created_at >= start).all()
    except Exception:
        return [k.strftime("%d %b") for k in keys], [0] * days
    for row in rows:
        if row.created_at:
            stamp = row.created_at.date().isoformat()
            if stamp in buckets:
                buckets[stamp] += 1
    return [k.strftime("%d %b") for k in keys], [buckets[k.isoformat()] for k in keys]

AREAS = ["oral", "music", "dance", "poetry", "craft", "diaspora"]
AREA_LABELS = {
    "oral": "Oral History",
    "music": "Music & Song",
    "dance": "Dance & Movement",
    "poetry": "Poetry & Storytelling",
    "craft": "Craft & Cultural Practice",
    "diaspora": "Diaspora Connection",
}


def log_action(action, item=""):
    db.session.add(
        ActivityLog(action=action, item=(item or "")[:200], admin_name=current_user.name if current_user.is_authenticated else "Admin")
    )


def setting(key, default=""):
    row = SiteSetting.query.filter_by(key=key).first()
    return row.value if row else default


def set_setting(key, value):
    row = SiteSetting.query.filter_by(key=key).first()
    if not row:
        row = SiteSetting(key=key, value=value)
        db.session.add(row)
    else:
        row.value = value


def report_label(report):
    if report.item_type == "profile":
        obj = db.session.get(CulturalProfile, report.item_id)
        return obj.display_name if obj else f"Profile #{report.item_id}"
    if report.item_type == "story":
        obj = db.session.get(Voice, report.item_id) or db.session.get(StorySubmission, report.item_id)
        return obj.title if obj else f"Story #{report.item_id}"
    if report.item_type == "library":
        obj = db.session.get(LibraryItem, report.item_id)
        return obj.title if obj else f"Library #{report.item_id}"
    return f"{report.item_type} #{report.item_id}"


@admin_bp.route("/")
@admin_required
def dashboard():
    pending = StorySubmission.query.filter_by(status="pending").count()
    reports_open = ContentReport.query.filter(ContentReport.status.in_(["new", "open", "under_review"])).count()
    profiles_review = CulturalProfile.query.filter_by(moderation_status="under_review").count()
    unread = ContactMessage.query.filter_by(is_read=False).count()
    area_counts = [CulturalProfile.query.filter_by(area=a).count() for a in AREAS]
    status_counts = [
        StorySubmission.query.filter_by(status=s).count() for s in ("pending", "approved", "published", "rejected")
    ]
    labels, stories_series = _count_by_day(StorySubmission)
    _, library_series = _count_by_day(LibraryItem)
    _, profile_series = _count_by_day(CulturalProfile)
    _, collab_series = _count_by_day(CollaborationRequest)
    logs = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(8).all()
    recent_reports = ContentReport.query.order_by(ContentReport.created_at.desc()).limit(6).all()
    stats = {
        "people": CulturalProfile.query.count(),
        "works": PortfolioItem.query.count() + LibraryItem.query.count(),
        "pending": pending,
        "published": Voice.query.filter_by(status="published").count(),
        "collabs": CollaborationRequest.query.count(),
        "reports": reports_open,
    }
    return render_template(
        "admin/dashboard.html",
        stats=stats,
        pending=pending,
        reports_open=reports_open,
        profiles_review=profiles_review,
        unread=unread,
        area_counts=area_counts,
        area_labels=[AREA_LABELS[a] for a in AREAS],
        status_counts=status_counts,
        chart_labels=labels,
        stories_series=stories_series,
        library_series=library_series,
        profile_series=profile_series,
        collab_series=collab_series,
        recent_reports=recent_reports,
        report_label=report_label,
        logs=logs,
    )


@admin_bp.route("/search")
@admin_required
def search():
    q = (request.args.get("q") or "").strip()
    people = stories = items = []
    if q:
        like = f"%{q}%"
        people = CulturalProfile.query.filter(CulturalProfile.display_name.ilike(like)).limit(8).all()
        stories = StorySubmission.query.filter(StorySubmission.title.ilike(like)).limit(8).all()
        items = LibraryItem.query.filter(LibraryItem.title.ilike(like)).limit(8).all()
    return render_template("admin/search.html", q=q, people=people, stories=stories, items=items)


@admin_bp.route("/stories")
@admin_required
def stories():
    status = request.args.get("status", "all")
    q = (request.args.get("q") or "").strip().lower()
    category = request.args.get("category", "all")
    query = StorySubmission.query
    if status and status != "all":
        query = query.filter_by(status=status)
    if category and category != "all":
        query = query.filter_by(category=category)
    submissions = query.order_by(StorySubmission.created_at.desc()).all()
    if q:
        submissions = [s for s in submissions if q in (s.title + s.name + s.category).lower()]
    return render_template("admin/stories.html", submissions=submissions, status=status, q=q, category=category)


@admin_bp.route("/stories/<int:story_id>")
@admin_required
def story_review(story_id):
    submission = db.session.get(StorySubmission, story_id)
    if not submission:
        flash("Submission not found.", "error")
        return redirect(url_for("admin.stories"))
    return render_template("admin/story_review.html", submission=submission)


@admin_bp.route("/stories/<int:story_id>/approve")
@admin_required
def approve_story(story_id):
    submission = db.session.get(StorySubmission, story_id)
    if not submission:
        return redirect(url_for("admin.stories"))
    if not submission.consent:
        flash("Do not approve without confirmed consent.", "error")
        return redirect(url_for("admin.story_review", story_id=story_id))
    submission.status = "approved"
    submission.admin_notes = request.args.get("reason") or "Approved after consent and cultural-sensitivity review."
    log_action("Submission approved", submission.title)
    db.session.commit()
    flash(f'"{submission.title}" approved. You can now publish it to Voices.', "success")
    return redirect(url_for("admin.story_review", story_id=story_id))


@admin_bp.route("/stories/<int:story_id>/publish")
@admin_required
def publish_story(story_id):
    submission = db.session.get(StorySubmission, story_id)
    if not submission or submission.status != "approved":
        flash("Only approved stories can be published.", "error")
        return redirect(url_for("admin.stories"))
    if not submission.consent:
        flash("Consent must be confirmed before publication.", "error")
        return redirect(url_for("admin.story_review", story_id=story_id))
    submission.status = "published"
    submission.published_at = utcnow()
    db.session.add(
        Voice(
            title=submission.title,
            contributor=submission.name,
            category=submission.category,
            content=submission.content,
            credit_role=submission.credit_role,
            credit_name=submission.credit_name,
            consent_level=submission.consent_level,
            is_featured=False,
            status="published",
            moderation_status="active",
        )
    )
    log_action("Story published", submission.title)
    db.session.commit()
    flash(f'"{submission.title}" has been published to the Voices archive.', "success")
    return redirect(url_for("admin.stories"))


@admin_bp.route("/stories/<int:story_id>/reject", methods=["POST"])
@admin_required
def reject_story(story_id):
    submission = db.session.get(StorySubmission, story_id)
    reason = (request.form.get("reason") or "").strip()
    if submission and reason:
        submission.status = "rejected"
        submission.admin_notes = reason
        log_action("Submission rejected", submission.title)
        db.session.commit()
        flash("Submission rejected.", "info")
    else:
        flash("A reason is required.", "error")
    return redirect(url_for("admin.story_review", story_id=story_id) if submission else url_for("admin.stories"))


@admin_bp.route("/stories/<int:story_id>/changes", methods=["POST"])
@admin_required
def request_changes(story_id):
    submission = db.session.get(StorySubmission, story_id)
    reason = (request.form.get("reason") or "").strip()
    if submission and reason:
        submission.status = "changes"
        submission.admin_notes = reason
        log_action("Changes requested", submission.title)
        db.session.commit()
        flash("Change request sent.", "info")
    else:
        flash("A reason is required.", "error")
    return redirect(url_for("admin.story_review", story_id=story_id) if submission else url_for("admin.stories"))


@admin_bp.route("/people", methods=["GET"])
@admin_required
def people():
    profiles = CulturalProfile.query.order_by(CulturalProfile.display_name).all()
    counts = {p.id: PortfolioItem.query.filter_by(profile_id=p.id).count() for p in profiles}
    return render_template("admin/people.html", profiles=profiles, counts=counts, area_labels=AREA_LABELS)


@admin_bp.route("/people/new", methods=["GET", "POST"])
@admin_required
def people_new():
    return _save_person(None)


@admin_bp.route("/people/<int:profile_id>/edit", methods=["GET", "POST"])
@admin_required
def people_edit(profile_id):
    profile = db.session.get(CulturalProfile, profile_id)
    if not profile:
        return redirect(url_for("admin.people"))
    return _save_person(profile)


def _save_person(profile):
    if request.method == "POST":
        created = profile is None
        if created:
            profile = CulturalProfile(is_demo=False, is_public=True)
            db.session.add(profile)
        profile.display_name = request.form.get("display_name", "").strip()
        profile.profile_kind = request.form.get("profile_kind", "individual")
        profile.area = request.form.get("area", "oral")
        profile.bio = request.form.get("bio", "").strip()
        profile.location = request.form.get("location", "").strip()
        profile.website = request.form.get("website", "").strip()
        profile.social_link = request.form.get("social_link", "").strip()
        profile.skills = request.form.get("practices", "").strip()
        profile.source_info = request.form.get("source_info", "").strip()
        profile.curated = request.form.get("curated") == "on"
        profile.moderation_status = request.form.get("moderation_status", profile.moderation_status or "active")
        photo = request.files.get("photo")
        if photo and photo.filename:
            name = secure_filename(photo.filename)
            dest = Path(current_app.config["UPLOAD_FOLDER"]) / "profiles"
            dest.mkdir(parents=True, exist_ok=True)
            photo.save(dest / name)
            profile.photo = name
        log_action("Profile created" if created else "Profile edited", profile.display_name)
        db.session.commit()
        flash("Profile saved.", "success")
        return redirect(url_for("admin.people"))
    return render_template(
        "admin/person_form.html",
        profile=profile,
        kinds=PROFILE_KINDS,
        statuses=PROFILE_STATUSES,
        areas=get_areas("en"),
    )


@admin_bp.route("/people/<int:profile_id>/action/<action>")
@admin_required
def people_action(profile_id, action):
    profile = db.session.get(CulturalProfile, profile_id)
    if not profile:
        return redirect(url_for("admin.people"))
    if action == "curate":
        profile.curated = True
        log_action("Profile curated", profile.display_name)
    elif action == "uncurate":
        profile.curated = False
        log_action("Curated status removed", profile.display_name)
    elif action == "review":
        profile.moderation_status = "under_review"
        log_action("Profile under review", profile.display_name)
    elif action == "suspend":
        profile.moderation_status = "suspended"
        log_action("Profile suspended", profile.display_name)
    elif action == "restore":
        profile.moderation_status = "active"
        log_action("Profile restored", profile.display_name)
    elif action == "archive":
        profile.moderation_status = "archived"
        profile.is_public = False
        log_action("Profile archived", profile.display_name)
    db.session.commit()
    flash("Profile updated.", "success")
    return redirect(url_for("admin.people"))


@admin_bp.route("/library")
@admin_required
def library():
    kind = request.args.get("type", "All")
    query = LibraryItem.query
    named = {"Documentary", "Booklet", "Magazine", "Audio", "Video"}
    if kind in named:
        query = query.filter_by(content_type=kind)
    elif kind == "Other":
        query = query.filter(~LibraryItem.content_type.in_(named))
    items = query.order_by(LibraryItem.created_at.desc()).all()
    return render_template(
        "admin/library.html",
        items=items,
        area_labels=AREA_LABELS,
        kind=kind,
        tabs=LIBRARY_TABS,
    )


@admin_bp.route("/library/new", methods=["GET", "POST"])
@admin_required
def library_new():
    return _save_library(None)


@admin_bp.route("/library/<int:item_id>/edit", methods=["GET", "POST"])
@admin_required
def library_edit(item_id):
    item = db.session.get(LibraryItem, item_id)
    if not item:
        return redirect(url_for("admin.library"))
    return _save_library(item)


def _save_library(item):
    if request.method == "POST":
        created = item is None
        if created:
            item = LibraryItem()
            db.session.add(item)
        item.title = request.form.get("title", "").strip()
        item.content_type = request.form.get("content_type", "Other")
        item.area = request.form.get("area", "oral")
        item.short_description = request.form.get("short_description", "").strip()
        item.full_description = request.form.get("full_description", "").strip()
        item.author = request.form.get("author", "").strip()
        item.original_source = request.form.get("original_source", "").strip()
        item.community = request.form.get("community", "").strip()
        item.publication_date = request.form.get("publication_date", "").strip()
        item.location = request.form.get("location", "").strip()
        item.language = request.form.get("language", "").strip()
        item.external_link = request.form.get("external_link", "").strip()
        item.keywords = request.form.get("keywords", "").strip()
        item.cultural_context = request.form.get("cultural_context", "").strip()
        item.credits = request.form.get("credits", "").strip()
        item.rights = request.form.get("rights", "").strip()
        item.consent = request.form.get("consent") == "on"
        item.visibility = request.form.get("visibility", "draft")
        item.status = request.form.get("status", "draft")
        cover = request.files.get("cover")
        if cover and cover.filename:
            item.cover_name = secure_filename(cover.filename)
        media = request.files.get("file")
        if media and media.filename:
            item.file_name = secure_filename(media.filename)
        log_action("Publication added" if created else "Library item edited", item.title)
        db.session.commit()
        flash("Library item saved. Only the file name is stored in this prototype.", "success")
        return redirect(url_for("admin.library"))
    return render_template(
        "admin/library_form.html",
        item=item,
        types=LIBRARY_TYPES,
        vis=LIBRARY_VISIBILITY,
        areas=get_areas("en"),
    )


@admin_bp.route("/library/<int:item_id>/action/<action>")
@admin_required
def library_action(item_id, action):
    item = db.session.get(LibraryItem, item_id)
    if not item:
        return redirect(url_for("admin.library"))
    if action == "publish":
        item.status = "published"
        item.visibility = "public"
        log_action("Library item published", item.title)
    elif action == "unpublish":
        item.status = "unpublished"
        item.visibility = "draft"
        log_action("Library item unpublished", item.title)
    elif action == "archive":
        item.status = "archived"
        item.visibility = "private"
        log_action("Library item archived", item.title)
    elif action == "delete":
        title = item.title
        db.session.delete(item)
        log_action("Library item removed", title)
        db.session.commit()
        flash("Item removed.", "info")
        return redirect(url_for("admin.library"))
    db.session.commit()
    flash("Library item updated.", "success")
    return redirect(url_for("admin.library"))


@admin_bp.route("/projects", methods=["GET", "POST"])
@admin_required
def projects():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if title:
            db.session.add(
                Project(
                    title=title,
                    description=request.form.get("description", "").strip(),
                    category=request.form.get("category", "education"),
                    area=request.form.get("area", ""),
                    status=request.form.get("status", "planned"),
                    start_date=request.form.get("start_date", ""),
                    end_date=request.form.get("end_date", ""),
                    is_public=request.form.get("is_public") == "on",
                )
            )
            log_action("Project created", title)
            db.session.commit()
            flash("Project added.", "success")
        return redirect(url_for("admin.projects"))
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template(
        "admin/projects.html",
        projects=projects,
        statuses=PROJECT_STATUSES,
        areas=get_areas("en"),
    )


@admin_bp.route("/projects/<int:project_id>/edit", methods=["POST"])
@admin_required
def project_edit(project_id):
    project = db.session.get(Project, project_id)
    if project:
        project.title = request.form.get("title", project.title)
        project.description = request.form.get("description", project.description)
        project.status = request.form.get("status", project.status)
        project.area = request.form.get("area", project.area)
        project.start_date = request.form.get("start_date", "")
        project.end_date = request.form.get("end_date", "")
        project.is_public = request.form.get("is_public") == "on"
        log_action("Project edited", project.title)
        db.session.commit()
        flash("Project updated.", "success")
    return redirect(url_for("admin.projects"))


@admin_bp.route("/moderation")
@admin_required
def moderation():
    tab = request.args.get("tab", "all")
    query = ContentReport.query
    if tab == "reported":
        query = query.filter(ContentReport.status.in_(["new", "open"]))
    elif tab == "review":
        query = query.filter_by(status="under_review")
    elif tab == "resolved":
        query = query.filter(ContentReport.status.in_(["resolved", "dismissed", "action_required"]))
    reports = query.order_by(ContentReport.created_at.desc()).all()
    counts = {
        "all": ContentReport.query.count(),
        "reported": ContentReport.query.filter(ContentReport.status.in_(["new", "open"])).count(),
        "review": ContentReport.query.filter_by(status="under_review").count(),
        "suspended": CulturalProfile.query.filter_by(moderation_status="suspended").count()
        + Voice.query.filter_by(moderation_status="suspended").count()
        + LibraryItem.query.filter_by(status="suspended").count(),
        "resolved": ContentReport.query.filter(ContentReport.status.in_(["resolved", "dismissed"])).count(),
    }
    return render_template(
        "admin/moderation.html",
        reports=reports,
        report_label=report_label,
        reasons=dict(REPORT_REASONS),
        tab=tab,
        counts=counts,
    )


@admin_bp.route("/moderation/<int:report_id>")
@admin_required
def report_inspect(report_id):
    report = db.session.get(ContentReport, report_id)
    if not report:
        return redirect(url_for("admin.moderation"))
    if report.status == "new":
        report.status = "under_review"
        report.updated_at = utcnow()
        db.session.commit()
    return render_template(
        "admin/report_inspect.html",
        report=report,
        label=report_label(report),
        reasons=dict(REPORT_REASONS),
    )


@admin_bp.route("/moderation/<int:report_id>/decide", methods=["POST"])
@admin_required
def report_decide(report_id):
    report = db.session.get(ContentReport, report_id)
    if not report:
        return redirect(url_for("admin.moderation"))
    decision = request.form.get("decision")
    reason = (request.form.get("reason") or "").strip()
    report.decision = decision
    report.decision_reason = reason
    report.updated_at = utcnow()
    target_status = None
    if decision == "restore":
        report.status = "resolved"
        target_status = "active"
        log_action("Report dismissed / content restored", report_label(report))
    elif decision == "changes":
        report.status = "action_required"
        log_action("Changes requested after report", report_label(report))
    elif decision == "suspend":
        report.status = "under_review"
        target_status = "suspended"
        log_action("Content suspended", report_label(report))
    elif decision == "archive":
        report.status = "resolved"
        target_status = "archived"
        log_action("Content archived", report_label(report))
    elif decision == "remove":
        if not reason:
            flash("A reason is required before permanent removal.", "error")
            return redirect(url_for("admin.report_inspect", report_id=report_id))
        report.status = "resolved"
        target_status = "removed"
        log_action("Content removed", report_label(report))
    elif decision == "dismiss":
        report.status = "dismissed"
        target_status = "active"
        log_action("Report dismissed", report_label(report))
    _apply_moderation(report, target_status)
    db.session.commit()
    flash("Moderation decision saved. Inspect first is the rule — reports never auto-delete.", "success")
    return redirect(url_for("admin.moderation"))


def _apply_moderation(report, target_status):
    if not target_status:
        return
    if report.item_type == "profile":
        obj = db.session.get(CulturalProfile, report.item_id)
        if not obj:
            return
        if target_status == "removed":
            obj.moderation_status = "archived"
            obj.is_public = False
        elif target_status == "archived":
            obj.moderation_status = "archived"
            obj.is_public = False
        else:
            obj.moderation_status = target_status
    elif report.item_type == "story":
        obj = db.session.get(Voice, report.item_id)
        if obj:
            obj.moderation_status = "active" if target_status == "active" else "suspended"
            if target_status in {"removed", "archived"}:
                obj.status = "unpublished"
    elif report.item_type == "library":
        obj = db.session.get(LibraryItem, report.item_id)
        if obj:
            if target_status == "active":
                obj.status = "published"
                obj.visibility = "public"
            elif target_status == "suspended":
                obj.status = "suspended"
            else:
                obj.status = "archived"
                obj.visibility = "private"


@admin_bp.route("/contacts")
@admin_required
def contacts():
    tab = request.args.get("tab", "all")
    query = ContactMessage.query
    if tab == "unread":
        query = query.filter((ContactMessage.is_read == False) | (ContactMessage.inbox_status == "unread"))  # noqa: E712
    elif tab == "responded":
        query = query.filter_by(inbox_status="responded")
    elif tab == "archived":
        query = query.filter_by(inbox_status="archived")
    messages = query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("admin/contacts.html", messages=messages, tab=tab)


@admin_bp.route("/contacts/<int:message_id>/read")
@admin_required
def mark_contact_read(message_id):
    message = db.session.get(ContactMessage, message_id)
    if message:
        message.is_read = True
        message.inbox_status = "read"
        db.session.commit()
        flash("Message marked as read.", "success")
    return redirect(url_for("admin.contacts"))


@admin_bp.route("/contacts/<int:message_id>/action/<action>")
@admin_required
def contact_action(message_id, action):
    message = db.session.get(ContactMessage, message_id)
    if message:
        if action == "responded":
            message.inbox_status = "responded"
            message.is_read = True
        elif action == "archive":
            message.inbox_status = "archived"
        elif action == "delete":
            db.session.delete(message)
        db.session.commit()
    return redirect(url_for("admin.contacts"))


@admin_bp.route("/statistics")
@admin_required
def statistics():
    people = CulturalProfile.query.all()
    kinds = {
        "individual": sum(1 for p in people if p.profile_kind == "individual"),
        "troupe": sum(1 for p in people if p.profile_kind == "troupe"),
        "community_group": sum(1 for p in people if p.profile_kind == "community_group"),
        "organisation": sum(1 for p in people if p.profile_kind == "organisation"),
    }
    area_counts = [CulturalProfile.query.filter_by(area=a).count() for a in AREAS]
    lib = LibraryItem.query.all()
    type_counts = {}
    for item in lib:
        type_counts[item.content_type] = type_counts.get(item.content_type, 0) + 1
    collab_status = {
        "Pending": CollaborationRequest.query.filter_by(status="Pending").count(),
        "Accepted": CollaborationRequest.query.filter_by(status="Accepted").count(),
        "Declined": CollaborationRequest.query.filter_by(status="Declined").count(),
    }
    mod = {
        "new": ContentReport.query.filter(ContentReport.status.in_(["new", "open"])).count(),
        "under_review": ContentReport.query.filter_by(status="under_review").count(),
        "resolved": ContentReport.query.filter_by(status="resolved").count(),
        "dismissed": ContentReport.query.filter_by(status="dismissed").count(),
        "suspended": CulturalProfile.query.filter_by(moderation_status="suspended").count(),
    }
    type_labels = list(type_counts.keys()) or ["None yet"]
    type_values = list(type_counts.values()) or [0]
    collab_labels = list(collab_status.keys())
    collab_values = list(collab_status.values())
    return render_template(
        "admin/statistics.html",
        kinds=kinds,
        area_counts=area_counts,
        area_labels=[AREA_LABELS[a] for a in AREAS],
        type_labels=type_labels,
        type_values=type_values,
        collab_labels=collab_labels,
        collab_values=collab_values,
        collab_status=collab_status,
        mod=mod,
        stories=Voice.query.filter_by(status="published").count(),
        submissions=StorySubmission.query.count(),
        published_subs=StorySubmission.query.filter_by(status="published").count(),
        follows=Follow.query.count(),
        collabs=CollaborationRequest.query.count(),
        accepted=CollaborationRequest.query.filter_by(status="Accepted").count(),
        public_lib=LibraryItem.query.filter_by(visibility="public").count(),
        private_lib=LibraryItem.query.filter(LibraryItem.visibility.in_(["private", "members"])).count(),
        status_counts=[StorySubmission.query.filter_by(status=s).count() for s in ("pending", "approved", "published", "rejected")],
    )


@admin_bp.route("/metrics")
@admin_required
def metrics():
    return redirect(url_for("admin.statistics"))


@admin_bp.route("/activity")
@admin_required
def activity():
    logs = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(100).all()
    return render_template("admin/activity.html", logs=logs)


@admin_bp.route("/settings", methods=["GET", "POST"])
@admin_required
def settings():
    if request.method == "POST":
        set_setting("featured_group_id", request.form.get("featured_group_id", ""))
        set_setting("featured_voice_id", request.form.get("featured_voice_id", ""))
        log_action("Homepage featured content updated")
        db.session.commit()
        flash("Settings saved.", "success")
        return redirect(url_for("admin.settings"))
    groups = CulturalProfile.query.filter_by(profile_kind="troupe").all()
    voices = Voice.query.filter_by(status="published").all()
    return render_template(
        "admin/settings.html",
        groups=groups,
        voices=voices,
        featured_group_id=setting("featured_group_id"),
        featured_voice_id=setting("featured_voice_id"),
    )


@admin_bp.route("/subscribers")
@admin_required
def subscribers():
    return redirect(url_for("admin.contacts"))


@admin_bp.route("/mentorship")
@admin_required
def mentorship():
    return redirect(url_for("admin.moderation"))
