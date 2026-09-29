AREAS = [
    {
        "id": "oral",
        "name": "Oral History",
        "icon": "⌁",
        "meaning": "Spoken memory: family histories, proverbs, interviews and knowledge carried by voice.",
        "people": "Elders, family historians, interviewers, students documenting relatives, and people working with consent.",
        "preserve": "Spoken stories, written notes, and who is allowed to hear them.",
        "upload": "Written accounts, audio or video interview filenames, and cultural context notes.",
        "participate": "Submit an oral history to Voices, add an interview to your portfolio, or request a documented conversation.",
        "connect": "Request interviews, community documentation, or cultural research — never public phone numbers or emails.",
    },
    {
        "id": "music",
        "name": "Music & Song",
        "icon": "♪",
        "meaning": "Sound, rhythm and lyrics as identity, celebration, teaching and continuity.",
        "people": "Singers, instrumentalists, choirs, composers, and people who keep ceremonial or family songs.",
        "preserve": "Song meanings, performance settings, lyrics where sharing is allowed, and recordings of living practice.",
        "upload": "Audio/song portfolio items, video performances, written notes on when a song is sung.",
        "participate": "Publish a song story after review, list workshops, or show availability for events.",
        "connect": "Invite musicians for festivals, teaching, diaspora gatherings or collaborative recording.",
    },
    {
        "id": "dance",
        "name": "Dance & Movement",
        "icon": "↟",
        "meaning": "Movement as cultural knowledge, discipline, joy and collective memory.",
        "people": "Dancers, troupes, teachers, youth groups and choreographers working with traditional or contemporary forms.",
        "preserve": "Style notes, cultural meaning of steps, performance notes, photos, and workshop outlines.",
        "upload": "Performance videos, photos, workshop descriptions, and documentation of when dance is shared.",
        "participate": "Build a dance profile, add portfolio works, offer teaching or performances, and join the Creators directory.",
        "connect": "Receive collaboration requests for shows, school visits, festivals or community teaching.",
    },
    {
        "id": "poetry",
        "name": "Poetry & Storytelling",
        "icon": "✎",
        "meaning": "Creative language that holds emotion, history, humour and social reflection.",
        "people": "Poets, storytellers, spoken-word artists, writers and teachers.",
        "preserve": "Poems, story texts, performance notes, and language.",
        "upload": "Written story, poetry, spoken-word notes, and cultural background.",
        "participate": "Submit to Voices with consent, keep a writing portfolio, or offer school storytelling sessions.",
        "connect": "Collaborate on readings, publications, education programmes or diaspora events.",
    },
    {
        "id": "craft",
        "name": "Craft & Cultural Practice",
        "icon": "◈",
        "meaning": "Skills learned by making: objects, techniques, materials and the knowledge around them.",
        "people": "Makers, artisans, practitioners of everyday and ceremonial crafts, and teachers of making.",
        "preserve": "Process notes, material knowledge, photographs of work, and respect for designs that should not be copied.",
        "upload": "Photo/craft items, project notes, workshop offers, and documentation of technique.",
        "participate": "Show practice in a public profile, list workshops, or share notes with consent.",
        "connect": "Museum programmes, training, community projects and research — with consent and attribution.",
    },
    {
        "id": "diaspora",
        "name": "Diaspora Connection",
        "icon": "◎",
        "meaning": "How Rwandans abroad stay linked to language, ceremony, stories and people at home.",
        "people": "Diaspora families, cultural groups overseas, visitors, and practitioners in Rwanda who welcome exchange.",
        "preserve": "Migration stories, language practice abroad, event records, and links between home and host communities.",
        "upload": "Diaspora stories, event documentation, interviews, and collaboration notes (no private addresses).",
        "participate": "Share a diaspora story, list availability for diaspora events, or follow practitioners in Rwanda.",
        "connect": "Bridge requests for teaching, performances, research or community documentation across countries.",
    },
]

AVAIL_OPTIONS = [
    "performances",
    "workshops",
    "school visits",
    "mentorship",
    "interviews",
    "cultural research",
    "community projects",
    "museum programmes",
    "festivals",
    "diaspora events",
    "collaborations",
]

PORTFOLIO_TYPES = [
    "Video / Performance",
    "Audio / Song",
    "Written Story",
    "Poetry",
    "Photo / Craft",
    "Interview / Oral History",
    "Project",
    "Workshop",
    "Cultural documentation",
]

COLLAB_TYPES = [
    "Performance",
    "Workshop",
    "Interview",
    "Research",
    "School Visit",
    "Mentorship",
    "Event",
]

PROFILE_KINDS = [
    ("individual", "Individual"),
    ("troupe", "Cultural Troupe"),
    ("community_group", "Community Group"),
    ("organisation", "Organisation"),
]

LOCATIONS = [
    ("all", "All locations"),
    ("kigali", "Kigali"),
    ("huye", "Huye"),
    ("musanze", "Musanze"),
    ("nyamata", "Nyamata"),
    ("diaspora", "Diaspora / abroad"),
    ("unlisted", "Location not listed"),
]

EVENT_TYPES = [
    ("performance", "Performance"),
    ("workshop", "Workshop"),
    ("exhibition", "Exhibition"),
    ("gathering", "Cultural gathering"),
]

CONSENT_LEVELS = [
    ("public", "Public"),
    ("members", "Members only"),
    ("private", "Private archive"),
]

CREDIT_ROLES = [
    ("shared_by", "Shared by"),
    ("original", "Original practitioner"),
    ("community", "Community"),
    ("source", "Source"),
]

LIBRARY_TYPES = [
    "Documentary",
    "Booklet",
    "Pamphlet",
    "Magazine",
    "Notebook",
    "Research Document",
    "Oral History Recording",
    "Audio",
    "Video",
    "Photograph Collection",
    "Cultural Guide",
    "Article",
    "Educational Resource",
    "Other",
]

LIBRARY_VISIBILITY = [
    ("public", "Public"),
    ("members", "Members only"),
    ("private", "Private archive"),
    ("draft", "Draft"),
]

REPORT_REASONS = [
    ("inaccurate", "Incorrect cultural information"),
    ("copyright", "Copyright / ownership concern"),
    ("consent", "Missing consent"),
    ("inappropriate", "Offensive / inappropriate content"),
    ("misrepresentation", "Misrepresentation"),
    ("privacy", "Privacy concern"),
    ("spam", "Spam"),
    ("other", "Other"),
]

PROJECT_STATUSES = [
    ("planned", "Planned"),
    ("active", "Active"),
    ("completed", "Completed"),
    ("archived", "Archived"),
]

PROFILE_STATUSES = [
    ("active", "Active"),
    ("under_review", "Under Review"),
    ("suspended", "Suspended"),
    ("archived", "Archived"),
]

KNOWLEDGE = [
    {
        "id": "intore",
        "area": "dance",
        "title": "Intore",
        "summary": "A well-known Rwandan dance tradition associated with ceremony, discipline and collective pride.",
        "body": "Intore is often described as a warrior or heroic dance. Groups may perform it at community and cultural events. Steps, costume and meaning can vary by troupe and occasion. Teachers and troupes remain the guide — this is a short community note, not a textbook.",
    },
    {
        "id": "umushagiriro",
        "area": "dance",
        "title": "Umushagiriro",
        "summary": "A traditional Rwandan dance form, often presented with graceful, flowing movement.",
        "body": "Umushagiriro appears in community and troupe repertoires alongside other dances. How it is taught and when it is performed depends on the group. Learners should treat local teachers and practitioners as the authority for style and meaning.",
    },
    {
        "id": "ikinimba",
        "area": "dance",
        "title": "Ikinimba",
        "summary": "A traditional dance connected with celebration, work and community gathering in parts of Rwanda.",
        "body": "Ikinimba is part of living dance practice kept by troupes, youth groups and community teachers. Details of origin stories and regional style should be credited to practitioners rather than assumed from a short digital summary.",
    },
    {
        "id": "ingoma",
        "area": "music",
        "title": "Ingoma",
        "summary": "Drums used in Rwandan music, ceremony and performance.",
        "body": "Ingoma can accompany dance, mark ceremony, and carry rhythm for teaching and celebration. Drumming knowledge is often learned in groups. Recordings and notes should be shared only with consent, especially where ceremony is involved.",
    },
    {
        "id": "oral-history",
        "area": "oral",
        "title": "Oral history",
        "summary": "Spoken memory: family stories, proverbs, interviews and knowledge carried by voice.",
        "body": "Oral history is a core way communities keep culture when it is not only written down. UmucoPulse treats testimony as sensitive: consent, context and credit matter before anything is published to Voices.",
    },
    {
        "id": "crafts",
        "area": "craft",
        "title": "Traditional crafts",
        "summary": "Making as cultural knowledge: materials, technique, and designs that may need protection.",
        "body": "Craft practice includes everyday and ceremonial making. Some patterns or objects should not be copied without permission. Documentation on UmucoPulse is meant to respect makers, not extract designs.",
    },
    {
        "id": "storytelling",
        "area": "poetry",
        "title": "Poetry and storytelling",
        "summary": "Creative language that holds history, humour, teaching and social reflection.",
        "body": "Poems, ibisigo, spoken word and community stories can all live here. Contributors can share text, performance notes and language, then wait for review before anything is public.",
    },
    {
        "id": "diaspora-practice",
        "area": "diaspora",
        "title": "Culture across distance",
        "summary": "How people abroad stay linked to language, ceremony, stories and groups at home.",
        "body": "Diaspora families and cultural groups may host language practice, dance, remembrance and virtual sessions. UmucoPulse can help people discover groups and request collaboration without publishing private contact details.",
    },
]


def location_key_from_text(text):
    value = (text or "").lower()
    if "kigali" in value:
        return "kigali"
    if "huye" in value:
        return "huye"
    if "musanze" in value:
        return "musanze"
    if "nyamata" in value:
        return "nyamata"
    if "diaspora" in value or "mauritius" in value or "abroad" in value:
        return "diaspora"
    if not value.strip():
        return "unlisted"
    return "other"


def knowledge_by_id(entry_id):
    return next((item for item in KNOWLEDGE if item["id"] == entry_id), None)

AREAS_BASE = [{"id": item["id"], "icon": item["icon"]} for item in AREAS]


def area_name(area_id, lang="en"):
    from app.i18n import area_name as localized

    return localized(area_id, lang)
