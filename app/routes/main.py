from pathlib import Path

from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app.culture import (
    AVAIL_OPTIONS,
    COLLAB_TYPES,
    EVENT_TYPES,
    KNOWLEDGE,
    LOCATIONS,
    REPORT_REASONS,
    PORTFOLIO_TYPES,
    knowledge_by_id,
    location_key_from_text,
)
from app.extensions import db
from app.forms import ContactForm, MentorshipForm, NewsletterForm, ProjectFilterForm, StorySubmissionForm
from app.i18n import CONTACT_ROLES, area_name, get_areas, get_ui
from app.models import (
    CollaborationRequest,
    ContactMessage,
    ContentReport,
    CulturalEvent,
    CulturalProfile,
    Favourite,
    Follow,
    LibraryItem,
    MentorshipRequest,
    NewsletterSubscriber,
    Opportunity,
    PortfolioItem,
    Project,
    SiteSetting,
    StorySubmission,
    Voice,
)
from app.recommend import similar_profiles
from app.routes.auth import contributor_required

main_bp = Blueprint("main", __name__)


def _lang():
    return session.get("lang", "en")


def _area_name(area_id):
    return area_name(area_id, _lang())


def _live_profiles():
    return CulturalProfile.query.filter_by(is_public=True, moderation_status="active")


def _impact():
    profiles = _live_profiles()
    groups = profiles.filter(CulturalProfile.profile_kind.in_(["troupe", "community_group", "organisation"]))
    return {
        "creators": profiles.count(),
        "published": Voice.query.filter_by(status="published").count()
        + StorySubmission.query.filter_by(status="published").count(),
        "areas": len({p.area for p in profiles.all() if p.area}),
        "works": PortfolioItem.query.count(),
        "groups": groups.count(),
        "collabs": CollaborationRequest.query.filter_by(status="Accepted").count(),
        "events": CulturalEvent.query.filter_by(is_public=True).count(),
        "library": LibraryItem.query.filter_by(visibility="public").count(),
        "projects": Project.query.filter_by(is_public=True).count(),
    }


def _is_saved(item_type, item_id):
    if not current_user.is_authenticated:
        return False
    return (
        Favourite.query.filter_by(user_id=current_user.id, item_type=item_type, item_id=item_id).first()
        is not None
    )


@main_bp.route("/")
def index():
    featured_group = (
        _live_profiles().filter_by(profile_kind="troupe", display_name="Intayoberana Cultural Troupe").first()
        or _live_profiles().filter_by(profile_kind="troupe").first()
    )
    featured_creators = (
        _live_profiles()
        .order_by(CulturalProfile.curated.desc(), CulturalProfile.id)
        .limit(3)
        .all()
    )
    featured_voice = Voice.query.filter_by(status="published", is_featured=True, moderation_status="active").first() or Voice.query.filter_by(
        status="published", moderation_status="active"
    ).first()
    fg = SiteSetting.query.filter_by(key="featured_group_id").first()
    if fg and fg.value:
        chosen = db.session.get(CulturalProfile, int(fg.value))
        if chosen:
            featured_group = chosen
    fv = SiteSetting.query.filter_by(key="featured_voice_id").first()
    if fv and fv.value:
        chosen_v = db.session.get(Voice, int(fv.value))
        if chosen_v:
            featured_voice = chosen_v
    featured_stories = Voice.query.filter_by(status="published", moderation_status="active").order_by(Voice.created_at.desc()).limit(3).all()
    upcoming = CulturalEvent.query.filter_by(is_public=True).limit(3).all()
    return render_template(
        "index.html",
        areas=get_areas(_lang()),
        featured_creators=featured_creators,
        featured_stories=featured_stories,
        featured_group=featured_group,
        featured_voice=featured_voice,
        upcoming=upcoming,
        impact=_impact(),
        area_name=_area_name,
    )


@main_bp.route("/discover")
def discover():
    return render_template("discover.html", areas=get_areas(_lang()))


@main_bp.route("/discover/articles")
def discover_articles():
    return render_template("discover_articles.html")


@main_bp.route("/discover/articles/impact")
def discover_article_impact():
    return render_template("discover_article_impact.html", impact=_impact())


@main_bp.route("/library")
def library():
    items = LibraryItem.query.filter_by(visibility="public", status="published").order_by(LibraryItem.created_at.desc()).all()
    return render_template("library.html", items=items, area_name=_area_name)


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/mission")
def mission():
    return redirect(url_for("main.about"))


@main_bp.route("/voice")
def voice():
    cat = request.args.get("cat", "all")
    featured_q = Voice.query.filter_by(status="published", is_featured=True, moderation_status="active")
    community_q = Voice.query.filter_by(status="published", is_featured=False, moderation_status="active")
    if cat and cat != "all":
        featured_q = featured_q.filter_by(category=cat)
        community_q = community_q.filter_by(category=cat)
    voice_cats = [(a["id"], a["name"]) for a in get_areas(_lang()) if a["id"] in {"oral", "poetry", "music", "dance"}]
    return render_template(
        "voice.html",
        featured_voices=featured_q.all(),
        community_voices=community_q.order_by(Voice.created_at.desc()).all(),
        cat=cat,
        voice_cats=voice_cats,
    )


@main_bp.route("/projects")
def projects():
    form = ProjectFilterForm()
    category = request.args.get("category", "all")
    search = request.args.get("q", "").strip()
    query = Project.query.filter(Project.status != "archived")
    if category and category != "all":
        query = query.filter_by(category=category)
    if search:
        like = f"%{search}%"
        query = query.filter(Project.title.ilike(like) | Project.description.ilike(like))
    project_list = query.order_by(Project.created_at.desc()).all()
    form.category.data = category
    return render_template(
        "projects.html",
        projects=project_list,
        form=form,
        active_category=category,
        search=search,
    )


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    form.role.choices = CONTACT_ROLES.get(_lang(), CONTACT_ROLES["en"])
    if form.validate_on_submit():
        message = ContactMessage(
            name=form.name.data.strip(),
            email=form.email.data.strip().lower(),
            role=form.role.data,
            message=form.message.data.strip(),
        )
        db.session.add(message)
        db.session.commit()
        flash(get_ui(_lang()).get("contact_thanks", "Thank you."), "success")
        return redirect(url_for("main.contact"))
    return render_template("contact.html", form=form)


@main_bp.route("/mentorship", methods=["GET", "POST"])
def mentorship():
    form = MentorshipForm()
    if current_user.is_authenticated:
        form.name.data = form.name.data or current_user.name
        form.email.data = form.email.data or current_user.email
    if form.validate_on_submit():
        db.session.add(
            MentorshipRequest(
                name=form.name.data.strip(),
                email=form.email.data.strip().lower(),
                request_type=form.request_type.data,
                focus_area=form.focus_area.data,
                details=form.details.data.strip(),
            )
        )
        db.session.commit()
        flash("Your mentorship request has been recorded. An administrator will follow up.", "success")
        return redirect(url_for("main.mentorship"))
    return render_template("mentorship.html", form=form)


@main_bp.route("/submit-story", methods=["GET", "POST"])
@contributor_required
def submit_story():
    form = StorySubmissionForm()
    if form.validate_on_submit():
        submission = StorySubmission(
            user_id=current_user.id,
            name=current_user.name,
            email=current_user.email,
            title=form.title.data.strip(),
            category=form.category.data,
            story_type=form.story_type.data,
            content=form.content.data.strip(),
            consent=form.consent.data,
            consent_level=form.consent_level.data,
            credit_role=form.credit_role.data,
            credit_name=(form.credit_name.data or "").strip(),
            status="pending",
        )
        db.session.add(submission)
        db.session.commit()
        flash(
            "Story submitted successfully and sent for administrator review.",
            "success",
        )
        return redirect(url_for("main.dashboard"))
    return render_template("submit_story.html", form=form)


@main_bp.route("/dashboard")
@contributor_required
def dashboard():
    mine = (
        StorySubmission.query.filter_by(user_id=current_user.id)
        .order_by(StorySubmission.created_at.desc())
        .all()
    )
    stats = {
        "total": len(mine),
        "pending": sum(1 for s in mine if s.status == "pending"),
        "published": sum(1 for s in mine if s.status == "published"),
    }
    profile = CulturalProfile.query.filter_by(user_id=current_user.id).first()
    collabs = []
    works = []
    if profile:
        collabs = (
            CollaborationRequest.query.filter_by(to_profile_id=profile.id)
            .order_by(CollaborationRequest.created_at.desc())
            .all()
        )
        works = PortfolioItem.query.filter_by(profile_id=profile.id).all()
    ui = get_ui(_lang())
    similar = similar_profiles(
        profile,
        _live_profiles().all(),
        ui,
        _area_name,
        you_both=True,
        exclude_user_id=current_user.id,
    )
    return render_template(
        "dashboard.html",
        submissions=mine,
        stats=stats,
        profile=profile,
        collabs=collabs,
        works=works,
        similar=similar,
        area_name=_area_name,
    )


@main_bp.route("/saved")
@login_required
def saved():
    rows = Favourite.query.filter_by(user_id=current_user.id).order_by(Favourite.created_at.desc()).all()
    items = []
    for row in rows:
        title = f"{row.item_type} #{row.item_id}"
        url = None
        if row.item_type == "profile":
            obj = db.session.get(CulturalProfile, row.item_id)
            if obj:
                title = obj.display_name
                url = url_for("main.creator", profile_id=obj.id)
        elif row.item_type == "event":
            obj = db.session.get(CulturalEvent, row.item_id)
            if obj:
                title = obj.title
                url = url_for("main.events")
        elif row.item_type == "story":
            obj = db.session.get(Voice, row.item_id) or db.session.get(StorySubmission, row.item_id)
            if obj:
                title = obj.title
                url = url_for("main.voice")
        items.append({"kind": row.item_type, "title": title, "url": url})
    return render_template("saved.html", items=items)


@main_bp.route("/newsletter", methods=["POST"])
def newsletter():
    form = NewsletterForm()
    if not form.validate_on_submit():
        flash("Please enter a valid email address.", "error")
        return redirect(request.referrer or url_for("main.index"))

    email = form.email.data.strip().lower()
    existing = NewsletterSubscriber.query.filter_by(email=email).first()
    if existing:
        if not existing.is_active:
            existing.is_active = True
            db.session.commit()
            flash("Welcome back! You have been re-subscribed to our newsletter.", "success")
        else:
            flash("You are already subscribed to our newsletter.", "info")
    else:
        db.session.add(NewsletterSubscriber(email=email))
        db.session.commit()
        flash("Thank you for subscribing to UmucoPulse updates!", "success")

    return redirect(request.referrer or url_for("main.index"))


@main_bp.route("/language/<code>")
def set_language(code):
    if code not in {"en", "rw", "fr"}:
        code = "en"
    session["lang"] = code
    labels = {"en": "Language preference saved.", "rw": "Ururimi rwabitswe.", "fr": "Préférence de langue enregistrée."}
    flash(labels[code], "info")
    return redirect(request.referrer or url_for("main.index"))


def _ensure_profile(user):
    profile = CulturalProfile.query.filter_by(user_id=user.id).first()
    if not profile:
        profile = CulturalProfile(
            user_id=user.id,
            display_name=user.name,
            area="oral",
            is_public=False,
            is_demo=False,
            profile_kind="individual",
        )
        db.session.add(profile)
        db.session.commit()
    return profile


@main_bp.route("/creators")
def creators():
    area = request.args.get("area", "all")
    kind = request.args.get("kind", "all")
    location = request.args.get("location", "all")
    q = (request.args.get("q") or "").strip().lower()
    query = _live_profiles()
    if area and area != "all":
        query = query.filter_by(area=area)
    if kind and kind != "all":
        query = query.filter_by(profile_kind=kind)
    if location and location != "all":
        query = query.filter_by(location_key=location)
    profiles = query.order_by(CulturalProfile.display_name).all()
    if q:
        profiles = [
            p
            for p in profiles
            if q
            in (
                p.display_name
                + (p.role or "")
                + (p.location or "")
                + (p.bio or "")
                + (p.skills or "")
                + (p.community_note or "")
                + _area_name(p.area)
            ).lower()
        ]
    follow_ids = set()
    if current_user.is_authenticated:
        follow_ids = {f.profile_id for f in Follow.query.filter_by(follower_id=current_user.id).all()}
    counts = {
        p.id: (
            PortfolioItem.query.filter_by(profile_id=p.id).count(),
            Follow.query.filter_by(profile_id=p.id).count(),
        )
        for p in profiles
    }
    return render_template(
        "creators.html",
        profiles=profiles,
        area=area,
        kind=kind,
        location=location,
        q=q,
        follow_ids=follow_ids,
        counts=counts,
        area_name=_area_name,
        areas=get_areas(_lang()),
    )


@main_bp.route("/creators/<int:profile_id>")
def creator(profile_id):
    profile = db.session.get(CulturalProfile, profile_id)
    if not profile or not profile.is_public:
        flash("This cultural profile is private or was not found.", "info")
        return redirect(url_for("main.creators"))
    if (profile.moderation_status or "active") != "active":
        if not (current_user.is_authenticated and current_user.is_admin):
            return render_template("unavailable.html"), 403
    works = PortfolioItem.query.filter_by(profile_id=profile.id).all()
    followers = Follow.query.filter_by(profile_id=profile.id).count()
    following = False
    mine = False
    if current_user.is_authenticated:
        following = Follow.query.filter_by(follower_id=current_user.id, profile_id=profile.id).first() is not None
        mine = profile.user_id == current_user.id
    ui = get_ui(_lang())
    exclude_id = current_user.id if current_user.is_authenticated else None
    similar = similar_profiles(
        profile,
        _live_profiles().all(),
        ui,
        _area_name,
        you_both=bool(current_user.is_authenticated and not mine),
        exclude_user_id=exclude_id,
    )
    return render_template(
        "creator.html",
        profile=profile,
        works=works,
        followers=followers,
        following=following,
        mine=mine,
        area_name=_area_name,
        collab_types=COLLAB_TYPES,
        saved=_is_saved("profile", profile.id),
        host_events=CulturalEvent.query.filter_by(profile_id=profile.id, is_public=True).all(),
        report_reasons=REPORT_REASONS,
        similar=similar,
    )


@main_bp.route("/creators/<int:profile_id>/follow", methods=["POST"])
@login_required
def follow_creator(profile_id):
    profile = db.session.get(CulturalProfile, profile_id)
    if not profile or profile.user_id == current_user.id:
        return redirect(url_for("main.creators"))
    existing = Follow.query.filter_by(follower_id=current_user.id, profile_id=profile_id).first()
    if existing:
        db.session.delete(existing)
        flash("Unfollowed.", "info")
    else:
        db.session.add(Follow(follower_id=current_user.id, profile_id=profile_id))
        flash("You are now following this practitioner.", "success")
    db.session.commit()
    return redirect(request.referrer or url_for("main.creator", profile_id=profile_id))


@main_bp.route("/creators/<int:profile_id>/collaborate", methods=["POST"])
@login_required
def collaborate(profile_id):
    profile = db.session.get(CulturalProfile, profile_id)
    if not profile or profile.user_id == current_user.id:
        return redirect(url_for("main.creators"))
    message = (request.form.get("message") or "").strip()
    request_type = request.form.get("request_type") or "collaborations"
    if len(message) < 8:
        flash("Please write a short message explaining the invitation.", "error")
        return redirect(url_for("main.creator", profile_id=profile_id))
    db.session.add(
        CollaborationRequest(
            from_user_id=current_user.id,
            from_name=current_user.name,
            to_profile_id=profile_id,
            request_type=request_type,
            message=message,
            status="Pending",
        )
    )
    db.session.commit()
    flash("Collaboration request sent. Status starts as Pending.", "success")
    return redirect(url_for("main.creator", profile_id=profile_id))


@main_bp.route("/opportunities")
def opportunities():
    category = request.args.get("category", "all")
    query = Opportunity.query
    if category and category != "all":
        query = query.filter_by(category=category)
    items = query.order_by(Opportunity.id).all()
    return render_template("opportunities.html", items=items, category=category, collab_types=COLLAB_TYPES)


@main_bp.route("/profile", methods=["GET", "POST"])
@contributor_required
def profile():
    profile = _ensure_profile(current_user)
    if request.method == "POST" and request.form.get("form") == "profile":
        profile.display_name = request.form.get("display_name", profile.display_name).strip()
        profile.area = request.form.get("area", profile.area)
        profile.role = request.form.get("role", "").strip()
        profile.location = request.form.get("location", "").strip()
        profile.languages = request.form.get("languages", "").strip()
        profile.bio = request.form.get("bio", "").strip()
        profile.background = request.form.get("background", "").strip()
        profile.skills = request.form.get("skills", "").strip()
        profile.community_note = request.form.get("community_note", "").strip()
        profile.website = request.form.get("website", "").strip()
        kind = request.form.get("profile_kind", profile.profile_kind or "individual")
        if kind in {"individual", "troupe", "community_group", "organisation"}:
            profile.profile_kind = kind
        profile.location_key = location_key_from_text(profile.location)
        photo = request.files.get("photo")
        if photo and photo.filename:
            name = secure_filename(photo.filename)
            dest = Path(current_app.config["UPLOAD_FOLDER"]) / "profiles"
            dest.mkdir(parents=True, exist_ok=True)
            photo.save(dest / name)
            profile.photo = name
        profile.available = "|".join(request.form.getlist("available"))
        profile.is_public = request.form.get("is_public") == "on"
        db.session.commit()
        flash("Profile saved. Public profiles appear in People & Groups.", "success")
        return redirect(url_for("main.profile"))
    if request.method == "POST" and request.form.get("form") == "portfolio":
        f = request.files.get("media")
        db.session.add(
            PortfolioItem(
                profile_id=profile.id,
                title=request.form.get("title", "").strip(),
                item_type=request.form.get("item_type", PORTFOLIO_TYPES[0]),
                description=request.form.get("description", "").strip(),
                context=request.form.get("context", "").strip(),
                link=request.form.get("link", "").strip(),
                date_label=request.form.get("date_label", "").strip(),
                media_name=f.filename if f and f.filename else "",
            )
        )
        db.session.commit()
        flash("Portfolio item added. Only the file name is stored in this prototype.", "success")
        return redirect(url_for("main.profile"))
    works = PortfolioItem.query.filter_by(profile_id=profile.id).all()
    return render_template(
        "profile.html",
        profile=profile,
        works=works,
        areas=get_areas(_lang()),
        avail_options=AVAIL_OPTIONS,
        portfolio_types=PORTFOLIO_TYPES,
    )


@main_bp.route("/profile/portfolio/<int:item_id>/delete", methods=["POST"])
@contributor_required
def delete_portfolio(item_id):
    profile = _ensure_profile(current_user)
    item = db.session.get(PortfolioItem, item_id)
    if item and item.profile_id == profile.id:
        db.session.delete(item)
        db.session.commit()
        flash("Portfolio item removed.", "info")
    return redirect(url_for("main.profile"))


@main_bp.route("/collaborations/<int:req_id>/<action>", methods=["POST"])
@contributor_required
def set_collaboration(req_id, action):
    profile = _ensure_profile(current_user)
    item = db.session.get(CollaborationRequest, req_id)
    if item and item.to_profile_id == profile.id and action in {"Accepted", "Declined"}:
        item.status = action
        db.session.commit()
        flash("Collaboration request updated.", "success")
    return redirect(url_for("main.dashboard"))


@main_bp.route("/events")
def events():
    event_type = request.args.get("type", "all")
    location = request.args.get("location", "all")
    query = CulturalEvent.query.filter_by(is_public=True)
    if event_type and event_type != "all":
        query = query.filter_by(event_type=event_type)
    if location and location != "all":
        query = query.filter_by(location_key=location)
    items = query.order_by(CulturalEvent.id).all()
    hosts = {p.id: p for p in CulturalProfile.query.all()}
    return render_template(
        "events.html",
        items=items,
        hosts=hosts,
        event_type=event_type,
        location=location,
        event_types=EVENT_TYPES,
    )


@main_bp.route("/knowledge")
def knowledge():
    return render_template("knowledge.html", entries=KNOWLEDGE, areas=get_areas(_lang()))


@main_bp.route("/knowledge/<entry_id>")
def knowledge_entry(entry_id):
    entry = knowledge_by_id(entry_id)
    if not entry:
        return redirect(url_for("main.knowledge"))
    related = _live_profiles().filter_by(area=entry["area"]).limit(4).all()
    return render_template("knowledge.html", entries=KNOWLEDGE, active=entry, related=related, areas=get_areas(_lang()))


@main_bp.route("/learn")
def learn():
    return render_template(
        "learn.html",
        areas=get_areas(_lang()),
        entries=KNOWLEDGE,
        workshops=CulturalEvent.query.filter_by(event_type="workshop", is_public=True).all(),
    )


@main_bp.route("/diaspora")
def diaspora():
    groups = _live_profiles().filter_by(area="diaspora").all()
    events = CulturalEvent.query.filter_by(location_key="diaspora", is_public=True).all()
    return render_template("diaspora.html", groups=groups, events=events, area_name=_area_name)


@main_bp.route("/impact")
def impact():
    return render_template("impact.html", impact=_impact())


@main_bp.route("/save/<item_type>/<int:item_id>", methods=["POST"])
@login_required
def toggle_save(item_type, item_id):
    if item_type not in {"profile", "story", "event"}:
        return redirect(request.referrer or url_for("main.index"))
    row = Favourite.query.filter_by(user_id=current_user.id, item_type=item_type, item_id=item_id).first()
    if row:
        db.session.delete(row)
        flash("Removed from saved items.", "info")
    else:
        db.session.add(Favourite(user_id=current_user.id, item_type=item_type, item_id=item_id))
        flash("Saved.", "success")
    db.session.commit()
    return redirect(request.referrer or url_for("main.index"))


@main_bp.route("/report/<item_type>/<int:item_id>", methods=["POST"])
def report_content(item_type, item_id):
    if item_type not in {"profile", "story", "event", "library"}:
        return redirect(request.referrer or url_for("main.index"))
    reason = (request.form.get("reason") or "inaccurate").strip()[:80]
    details = (request.form.get("details") or "").strip()
    reporter = current_user.name if current_user.is_authenticated else "Visitor"
    db.session.add(
        ContentReport(
            item_type=item_type,
            item_id=item_id,
            reason=reason,
            details=details,
            reporter=reporter,
            status="new",
        )
    )
    db.session.commit()
    flash(get_ui(_lang()).get("report_sent", "Report received."), "success")
    return redirect(request.referrer or url_for("main.index"))
