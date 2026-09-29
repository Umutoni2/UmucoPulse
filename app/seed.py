from sqlalchemy import inspect, text

from app.models import (
    CulturalEvent,
    CulturalProfile,
    FocusMetric,
    LibraryItem,
    Opportunity,
    PortfolioItem,
    Project,
    Skill,
    User,
    Voice,
)
from app.culture import location_key_from_text
from app.extensions import db
from flask import current_app


DANCE_TROUPES = [
    dict(
        display_name="Inyamibwa Cultural Troupe (ICT)",
        area="dance",
        profile_kind="troupe",
        role="Cultural Organisation",
        location="Kigali",
        languages="",
        bio="Music and dance focused on unity and healing.",
        background="Founded in 1998.",
        community_note="Over 100 members.",
        skills="Music, dance",
        available="",
        website="",
        photo="",
        curated=True,
        is_demo=False,
        is_public=True,
    ),
    dict(
        display_name="Inganzo Ngari",
        area="dance",
        profile_kind="troupe",
        role="Cultural Organisation",
        location="",
        languages="",
        bio="Traditional dance and folkloric group with strong youth and international visibility.",
        background="Formed in 2006.",
        community_note="",
        skills="Traditional dance, folklore",
        available="",
        website="",
        photo="",
        curated=True,
        is_demo=False,
        is_public=True,
    ),
    dict(
        display_name="Intayoberana Cultural Troupe",
        area="dance",
        profile_kind="troupe",
        role="Cultural Organisation",
        location="",
        languages="",
        bio="Traditional Rwandan cultural troupe",
        background="",
        community_note="Includes the children's cultural group Uruyange.",
        skills="Intore, Umushagiriro, Ikinimba",
        available="",
        website="",
        photo="",
        curated=True,
        is_demo=False,
        is_public=True,
    ),
    dict(
        display_name="Indinzi Cultural Troupe",
        area="dance",
        profile_kind="troupe",
        role="Cultural Organisation",
        location="",
        languages="",
        bio="Combines dance, drumming, storytelling and community teaching.",
        background="",
        community_note="",
        skills="Dance, drumming, storytelling, community teaching",
        available="",
        website="",
        photo="",
        curated=True,
        is_demo=False,
        is_public=True,
    ),
]


FOUNDER_PROFILE = dict(
    display_name="Umutoni Rutaganira Sylvie",
    area="poetry",
    profile_kind="individual",
    role="Founder of UmucoPulse",
    location="",
    languages="",
    bio="Started UmucoPulse as a student project for community cultural heritage. The platform is for the community, not a personal portfolio.",
    background="",
    community_note="",
    skills="",
    available="",
    website="",
    photo="",
    curated=True,
    is_demo=False,
    is_public=True,
)

INTAYOBERANA_WORKS = [
    "Traditional dance performances",
    "Intore performances",
    "Umushagiriro performances",
    "Ikinimba performances",
    "Youth/children's cultural performances",
]


def seed_database():
    ensure_profile_schema()
    if not User.query.first():
        _seed_core()
    _ensure_demo_contributor()
    _seed_community()
    _replace_dance_demos()
    _ensure_founder_profile()
    _ensure_location_keys()
    _ensure_events()
    _ensure_library()
    _refresh_public_copy()


def ensure_profile_schema():
    inspector = inspect(db.engine)
    if "cultural_profiles" not in inspector.get_table_names():
        return
    cols = {c["name"] for c in inspector.get_columns("cultural_profiles")}
    adds = []
    if "profile_kind" not in cols:
        adds.append("ALTER TABLE cultural_profiles ADD COLUMN profile_kind VARCHAR(40) DEFAULT 'individual'")
    if "website" not in cols:
        adds.append("ALTER TABLE cultural_profiles ADD COLUMN website VARCHAR(300) DEFAULT ''")
    if "photo" not in cols:
        adds.append("ALTER TABLE cultural_profiles ADD COLUMN photo VARCHAR(200) DEFAULT ''")
    if "community_note" not in cols:
        adds.append("ALTER TABLE cultural_profiles ADD COLUMN community_note TEXT DEFAULT ''")
    if "location_key" not in cols:
        adds.append("ALTER TABLE cultural_profiles ADD COLUMN location_key VARCHAR(40) DEFAULT 'unlisted'")
    if "moderation_status" not in cols:
        adds.append("ALTER TABLE cultural_profiles ADD COLUMN moderation_status VARCHAR(20) DEFAULT 'active'")
    if "source_info" not in cols:
        adds.append("ALTER TABLE cultural_profiles ADD COLUMN source_info VARCHAR(300) DEFAULT ''")
    if "social_link" not in cols:
        adds.append("ALTER TABLE cultural_profiles ADD COLUMN social_link VARCHAR(300) DEFAULT ''")
    if adds:
        with db.engine.begin() as conn:
            for sql in adds:
                conn.execute(text(sql))
    _ensure_column("story_submissions", "consent_level", "VARCHAR(20) DEFAULT 'public'")
    _ensure_column("story_submissions", "credit_role", "VARCHAR(40) DEFAULT 'shared_by'")
    _ensure_column("story_submissions", "credit_name", "VARCHAR(120) DEFAULT ''")
    _ensure_column("voices", "credit_role", "VARCHAR(40) DEFAULT 'shared_by'")
    _ensure_column("voices", "credit_name", "VARCHAR(120) DEFAULT ''")
    _ensure_column("voices", "consent_level", "VARCHAR(20) DEFAULT 'public'")
    _ensure_column("voices", "moderation_status", "VARCHAR(20) DEFAULT 'active'")
    _ensure_column("projects", "area", "VARCHAR(40) DEFAULT ''")
    _ensure_column("projects", "status", "VARCHAR(20) DEFAULT 'active'")
    _ensure_column("projects", "start_date", "VARCHAR(40) DEFAULT ''")
    _ensure_column("projects", "end_date", "VARCHAR(40) DEFAULT ''")
    _ensure_column("projects", "is_public", "BOOLEAN DEFAULT 1")
    _ensure_column("contact_messages", "inbox_status", "VARCHAR(20) DEFAULT 'unread'")
    _ensure_column("contact_messages", "source", "VARCHAR(40) DEFAULT 'contact'")
    _ensure_column("contact_messages", "subject", "VARCHAR(200) DEFAULT ''")
    _ensure_column("content_reports", "reporter", "VARCHAR(120) DEFAULT ''")
    _ensure_column("content_reports", "decision", "VARCHAR(40) DEFAULT ''")
    _ensure_column("content_reports", "decision_reason", "TEXT DEFAULT ''")
    _ensure_column("content_reports", "updated_at", "DATETIME")
    _migrate_report_status()


def _migrate_report_status():
    inspector = inspect(db.engine)
    if "content_reports" not in inspector.get_table_names():
        return
    with db.engine.begin() as conn:
        try:
            conn.execute(text("UPDATE content_reports SET status='new' WHERE status='open'"))
        except Exception:
            pass
        try:
            conn.execute(text("UPDATE cultural_profiles SET moderation_status='active' WHERE moderation_status IS NULL OR moderation_status=''"))
        except Exception:
            pass


def _ensure_column(table, column, ddl):
    inspector = inspect(db.engine)
    if table not in inspector.get_table_names():
        return
    cols = {c["name"] for c in inspector.get_columns(table)}
    if column in cols:
        return
    with db.engine.begin() as conn:
        conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {ddl}"))


def _ensure_demo_contributor():
    email = "sylvie@umucopulse.org"
    name = "Sylvie Umutoni Rutaganira"
    user = User.query.filter_by(email=email).first()
    old = User.query.filter_by(email="aline@umucopulse.org").first()
    if old and not user:
        old.email = email
        old.name = name
        old.role = "contributor"
        old.set_password("Story123!")
        db.session.commit()
        return
    if old and user:
        db.session.delete(old)
        db.session.commit()
    if user:
        if user.name != name:
            user.name = name
            db.session.commit()
        return
    contributor = User(email=email, name=name, role="contributor")
    contributor.set_password("Story123!")
    db.session.add(contributor)
    db.session.commit()


def _seed_core():
    admin = User(
        email=current_app.config["ADMIN_EMAIL"],
        name="UmucoPulse Administrator",
        role="admin",
    )
    admin.set_password(current_app.config["ADMIN_PASSWORD"])
    db.session.add(admin)

    contributor = User(
        email="sylvie@umucopulse.org",
        name="Sylvie Umutoni Rutaganira",
        role="contributor",
    )
    contributor.set_password("Story123!")
    db.session.add(contributor)

    projects = [
        Project(
            title="Heritage Workshops",
            description="Example project: a school or centre could list workshops here. This is not a running programme.",
            category="education",
            image="assets/workshops.svg",
            is_featured=True,
        ),
        Project(
            title="Voices Archive",
            description="Example project for keeping stories and recordings after consent. Not a national archive.",
            category="archive",
            image="assets/voices.svg",
            is_featured=True,
        ),
        Project(
            title="Performances & Events",
            description="Example project for a public sharing. Not a ticketed tour and not a confirmed booking.",
            category="performance",
            image="assets/music.svg",
            is_featured=True,
        ),
    ]
    db.session.add_all(projects)

    voices = [
        Voice(
            title="A poem (demo)",
            contributor="Demo story",
            category="poetry",
            quote="",
            content=(
                "This card is a sample. A real Voices piece would be the person’s own words — a poem, a memory, "
                "or a short note — after consent and review. It is not a published poet’s work."
            ),
            image="assets/poet.svg",
            is_featured=True,
            status="published",
        ),
        Voice(
            title="A dance note (demo)",
            contributor="Demo story",
            category="dance",
            content=(
                "This card is a sample. A dancer or troupe would write here, in their own words, what they share "
                "and when it is performed. It is not a real performance report."
            ),
            image="assets/dance.svg",
            is_featured=True,
            status="published",
        ),
        Voice(
            title="A song note (demo)",
            contributor="Demo story",
            category="music",
            content=(
                "This card is a sample. A musician would say what the song is for, when it is sung, and who may hear it. "
                "It is not a real recording or a national song list."
            ),
            image="assets/music.svg",
            is_featured=True,
            status="published",
        ),
    ]
    db.session.add_all(voices)

    metrics = [
        FocusMetric(name="workshops", label="Workshops listed (example target, not a real count)", value=0, target=0, icon="workshop"),
        FocusMetric(name="archive", label="Stories on this site (example target, not a real count)", value=0, target=0, icon="archive"),
        FocusMetric(name="artists", label="People in the directory (example target, not a real count)", value=0, target=0, icon="artist"),
    ]
    db.session.add_all(metrics)

    technical_skills = [
        ("C++", "technical", "Intermediate", 3, 1),
        ("Java", "technical", "Intermediate", 3, 2),
        ("Python", "technical", "Intermediate", 3, 3),
        ("C", "technical", "Beginner", 2, 4),
        ("JavaScript", "technical", "Beginner", 2, 5),
        ("HTML5", "technical", "Advanced", 4, 6),
        ("CSS3", "technical", "Advanced", 4, 7),
        ("Visual Basic", "technical", "Professional", 5, 8),
        ("Database Management", "technical", "Intermediate", 3, 9),
        ("Flask", "technical", "Intermediate", 3, 10),
    ]
    soft_skills = [
        ("Storytelling", "cultural", None, 0, 1),
        ("Workshop Facilitation", "cultural", None, 0, 2),
        ("Oral History Documentation", "cultural", None, 0, 3),
        ("Cultural Preservation", "cultural", None, 0, 4),
        ("Community Engagement", "cultural", None, 0, 5),
        ("Digital Archiving", "cultural", None, 0, 6),
        ("Performance Arts", "cultural", None, 0, 7),
        ("Event Planning", "cultural", None, 0, 8),
    ]
    for name, cat, level, rating, order in technical_skills + soft_skills:
        db.session.add(Skill(name=name, category=cat, level=level, rating=rating, sort_order=order))

    db.session.commit()


def _seed_community():
    if CulturalProfile.query.first():
        return

    demos = [
        dict(
            display_name="Demo Memory Keeper",
            area="oral",
            profile_kind="individual",
            role="Oral historian (prototype)",
            location="Huye, Rwanda",
            languages="Kinyarwanda, French",
            bio="Illustrative profile for recording family and community testimony with consent.",
            background="Demo content. Not a real person.",
            skills="Interviewing, transcription notes, community listening",
            available="interviews|cultural research|community projects",
        ),
        dict(
            display_name="Demo Inanga Circle",
            area="music",
            profile_kind="community_group",
            role="Musicians and song keepers",
            location="Musanze, Rwanda",
            languages="Kinyarwanda, English",
            bio="Prototype musicians showing how song meaning and performance notes can live beside a profile.",
            background="Fictional ensemble for the prototype.",
            skills="Song, accompaniment, cultural explanation",
            available="performances|workshops|diaspora events",
            curated=True,
        ),
        dict(
            display_name="Demo Spoken Word Studio",
            area="poetry",
            profile_kind="community_group",
            role="Poets and storytellers",
            location="Kigali, Rwanda",
            languages="Kinyarwanda, English, French",
            bio="Example writers documenting poems and storytelling for learners and community stages.",
            background="Demo identity for Poetry & Storytelling.",
            skills="Spoken word, classroom storytelling, bilingual performance",
            available="school visits|mentorship|festivals|collaborations",
        ),
        dict(
            display_name="Demo Agaseke Practice",
            area="craft",
            profile_kind="individual",
            role="Craft practitioners",
            location="Nyamata, Rwanda",
            languages="Kinyarwanda",
            bio="Illustrative makers profile: process, materials and teaching — not a real workshop brand.",
            background="Prototype content for Craft & Cultural Practice.",
            skills="Weaving knowledge, making demonstrations, documentation",
            available="workshops|museum programmes|community projects",
        ),
        dict(
            display_name="Demo Diaspora Circle",
            area="diaspora",
            profile_kind="community_group",
            role="Diaspora cultural organisers",
            location="Mauritius (demo location)",
            languages="English, French, Kinyarwanda",
            bio="Fictional diaspora group showing how people abroad can connect with practitioners in Rwanda.",
            background="Demo only. No real organisation is claimed.",
            skills="Event hosting, language practice, cultural exchange",
            available="diaspora events|collaborations|community projects",
        ),
    ]
    for item in demos:
        db.session.add(
            CulturalProfile(
                user_id=None,
                is_public=True,
                is_demo=True,
                **item,
            )
        )
    for item in DANCE_TROUPES:
        db.session.add(CulturalProfile(user_id=None, **item))

    db.session.add_all(
        [
            Opportunity(
                title="School cultural exchange session",
                category="school programmes",
                location="Open (prototype)",
                description="Illustrative call for practitioners willing to visit a classroom. Not a real school booking.",
                is_demo=True,
            ),
            Opportunity(
                title="Community documentation weekend",
                category="community projects",
                location="Rwanda (prototype)",
                description="Example of how a neighbourhood might invite oral historians. Demo listing only.",
                is_demo=True,
            ),
            Opportunity(
                title="Diaspora storytelling evening",
                category="diaspora programmes",
                location="Online / host city (prototype)",
                description="Fictional gathering format. Not an official event.",
                is_demo=True,
            ),
            Opportunity(
                title="Museum learning workshop (illustrative)",
                category="museum opportunities",
                location="To be confirmed",
                description="Shows how a cultural institution could later post a call. No partnership is claimed.",
                is_demo=True,
            ),
        ]
    )
    db.session.commit()
    _ensure_intayoberana_portfolio()


def _replace_dance_demos():
    demo_dance = CulturalProfile.query.filter_by(display_name="Demo Intore Ensemble").first()
    if demo_dance:
        PortfolioItem.query.filter_by(profile_id=demo_dance.id).delete()
        db.session.delete(demo_dance)
        db.session.commit()

    kinds = {
        "Demo Memory Keeper": "individual",
        "Demo Inanga Circle": "community_group",
        "Demo Spoken Word Studio": "community_group",
        "Demo Agaseke Practice": "individual",
        "Demo Diaspora Circle": "community_group",
    }
    for name, kind in kinds.items():
        row = CulturalProfile.query.filter_by(display_name=name).first()
        if row:
            row.profile_kind = kind

    for item in DANCE_TROUPES:
        existing = CulturalProfile.query.filter_by(display_name=item["display_name"]).first()
        if existing:
            for key, value in item.items():
                setattr(existing, key, value)
        else:
            db.session.add(CulturalProfile(user_id=None, **item))
    db.session.commit()
    _ensure_intayoberana_portfolio()


def _ensure_intayoberana_portfolio():
    troupe = CulturalProfile.query.filter_by(display_name="Intayoberana Cultural Troupe").first()
    if not troupe:
        return
    existing_titles = {w.title for w in PortfolioItem.query.filter_by(profile_id=troupe.id).all()}
    for title in INTAYOBERANA_WORKS:
        if title in existing_titles:
            continue
        db.session.add(
            PortfolioItem(
                profile_id=troupe.id,
                title=title,
                item_type="Performance",
                description="",
                context="",
            )
        )
    db.session.commit()


def _ensure_founder_profile():
    names = ("Umutoni Rutaganira Sylvie", "Sylvie Umutoni Rutaganira")
    existing = CulturalProfile.query.filter(CulturalProfile.display_name.in_(names)).first()
    if existing:
        for key, value in FOUNDER_PROFILE.items():
            setattr(existing, key, value)
    else:
        db.session.add(CulturalProfile(user_id=None, **FOUNDER_PROFILE))
    db.session.commit()


def _ensure_location_keys():
    for profile in CulturalProfile.query.all():
        profile.location_key = location_key_from_text(profile.location)
    db.session.commit()


def _ensure_events():
    if CulturalEvent.query.first():
        return
    hosts = {p.display_name: p for p in CulturalProfile.query.all()}
    intayo = hosts.get("Intayoberana Cultural Troupe")
    inyamibwa = hosts.get("Inyamibwa Cultural Troupe (ICT)")
    memory = hosts.get("Demo Memory Keeper")
    diaspora = hosts.get("Demo Diaspora Circle")
    events = [
        dict(
            title="Traditional dance sharing (illustrative listing)",
            event_type="performance",
            profile_id=intayo.id if intayo else None,
            location="Kigali",
            location_key="kigali",
            date_label="Prototype example",
            description="An example of how Intayoberana could list a public sharing of Intore, Umushagiriro or Ikinimba. This is not a confirmed real-world booking.",
            is_demo=True,
        ),
        dict(
            title="Community music and dance for unity (illustrative listing)",
            event_type="gathering",
            profile_id=inyamibwa.id if inyamibwa else None,
            location="Kigali",
            location_key="kigali",
            date_label="Prototype example",
            description="Example gathering format linked to Inyamibwa Cultural Troupe’s public focus on music, dance, unity and healing. Not a ticketed event claim.",
            is_demo=True,
        ),
        dict(
            title="Classroom oral-history listening session (demo)",
            event_type="workshop",
            profile_id=memory.id if memory else None,
            location="Huye",
            location_key="huye",
            date_label="Prototype example",
            description="Demo workshop showing how a school might invite careful listening and consent-based documentation.",
            is_demo=True,
        ),
        dict(
            title="Virtual diaspora cultural evening (demo)",
            event_type="gathering",
            profile_id=diaspora.id if diaspora else None,
            location="Online / host city",
            location_key="diaspora",
            date_label="Prototype example",
            description="Example of a diaspora gathering for language, memory and connection. Not an official programme.",
            is_demo=True,
        ),
    ]
    for item in events:
        db.session.add(CulturalEvent(**item))
    db.session.commit()


def _ensure_library():
    if LibraryItem.query.first():
        return
    db.session.add(
        LibraryItem(
            title="Intore teaching notes (prototype booklet)",
            content_type="Booklet",
            area="dance",
            short_description="An illustrative booklet record showing how a troupe could archive teaching notes with consent.",
            full_description="Prototype only. Not an official publication of any troupe. File storage in this demo keeps the file name, not the file.",
            author="UmucoPulse archive (demo)",
            original_source="Educational overview for the assignment prototype",
            community="",
            language="English / Kinyarwanda",
            keywords="intore, dance, education",
            cultural_context="Use with community teachers. This is not a complete or official ethnography.",
            credits="UmucoPulse prototype",
            rights="Demo record. No rights are claimed over real troupe materials.",
            consent=True,
            visibility="public",
            status="published",
            file_name="intore-notes-example.pdf",
        )
    )
    db.session.commit()


def _refresh_public_copy():
    voice_by_old = {
        "Featured Poet": dict(
            title="A poem (demo)",
            contributor="Demo story",
            quote="",
            content=(
                "This card is a sample. A real Voices piece would be the person’s own words — a poem, a memory, "
                "or a short note — after consent and review. It is not a published poet’s work."
            ),
        ),
        "Dance and Movement": dict(
            title="A dance note (demo)",
            contributor="Demo story",
            quote="",
            content=(
                "This card is a sample. A dancer or troupe would write here, in their own words, what they share "
                "and when it is performed. It is not a real performance report."
            ),
        ),
        "Stories and Song": dict(
            title="A song note (demo)",
            contributor="Demo story",
            quote="",
            content=(
                "This card is a sample. A musician would say what the song is for, when it is sung, and who may hear it. "
                "It is not a real recording or a national song list."
            ),
        ),
    }
    for old_title, fields in voice_by_old.items():
        row = Voice.query.filter_by(title=old_title).first()
        if row:
            for key, value in fields.items():
                setattr(row, key, value)
    project_text = {
        "Heritage Workshops": "Example project: a school or centre could list workshops here. This is not a running programme.",
        "Voices Archive": "Example project for keeping stories and recordings after consent. Not a national archive.",
        "Performances & Events": "Example project for a public sharing. Not a ticketed tour and not a confirmed booking.",
    }
    for title, description in project_text.items():
        row = Project.query.filter_by(title=title).first()
        if row:
            row.description = description
    metric_text = {
        "workshops": ("Workshops listed (example target, not a real count)", 0, 0),
        "archive": ("Stories on this site (example target, not a real count)", 0, 0),
        "artists": ("People in the directory (example target, not a real count)", 0, 0),
    }
    for name, (label, value, target) in metric_text.items():
        row = FocusMetric.query.filter_by(name=name).first()
        if row:
            row.label = label
            row.value = value
            row.target = target
    db.session.commit()
