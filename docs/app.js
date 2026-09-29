const DB = {
  users: "up2_users",
  session: "up2_session",
  submissions: "up2_submissions",
  contacts: "up2_contacts",
  subscribers: "up2_subscribers",
  projects: "up2_projects",
  profiles: "up2_profiles",
  portfolio: "up2_portfolio",
  follows: "up2_follows",
  collabs: "up2_collabs",
  opportunities: "up2_opportunities",
  events: "up2_events",
  favourites: "up2_favourites",
  reports: "up2_reports",
  library: "up2_library",
  activity: "up2_activity",
};

const AREAS = [
  {
    id: "oral",
    name: "Oral History",
    icon: "⌁",
    meaning: "Spoken memory: family histories, proverbs, interviews and knowledge carried by voice.",
    people: "Elders, family historians, interviewers, students documenting relatives, and people working with consent.",
    preserve: "Spoken stories, written notes, and who is allowed to hear them.",
    upload: "Written accounts, audio or video interview filenames, and cultural context notes (this prototype stores names and text, not the files).",
    participate: "Submit an oral history to Voices, add an interview to your portfolio, or request a documented conversation.",
    connect: "Request interviews, community documentation, or cultural research — never public phone numbers or emails.",
  },
  {
    id: "music",
    name: "Music & Song",
    icon: "♪",
    meaning: "Sound, rhythm and lyrics as identity, celebration, teaching and continuity.",
    people: "Singers, instrumentalists, choirs, composers, and people who keep ceremonial or family songs.",
    preserve: "Song meanings, performance settings, lyrics where sharing is allowed, and recordings of living practice.",
    upload: "Audio/song portfolio items, video performances, written notes on when a song is sung.",
    participate: "Publish a song story after review, list workshops, or show availability for events.",
    connect: "Invite musicians for festivals, teaching, diaspora gatherings or collaborative recording.",
  },
  {
    id: "dance",
    name: "Dance & Movement",
    icon: "↟",
    meaning: "Movement as cultural knowledge, discipline, joy and collective memory.",
    people: "Dancers, troupes, teachers, youth groups and choreographers working with traditional or contemporary forms.",
    preserve: "Style notes, cultural meaning of steps, performance video filenames, photos, and workshop outlines.",
    upload: "Performance videos, photos, workshop descriptions, and documentation of when dance is shared.",
    participate: "Build a dance profile, add portfolio works, offer teaching or performances, and join the Creators directory.",
    connect: "Receive collaboration requests for shows, school visits, festivals or community teaching.",
  },
  {
    id: "poetry",
    name: "Poetry & Storytelling",
    icon: "✎",
    meaning: "Creative language that holds emotion, history, humour and social reflection.",
    people: "Poets, storytellers, spoken-word artists, writers and teachers.",
    preserve: "Poems, story texts, performance notes, and language (Kinyarwanda, English, French or others).",
    upload: "Written story, poetry, spoken-word video filenames, and cultural background.",
    participate: "Submit to Voices with consent, keep a writing portfolio, or offer school storytelling sessions.",
    connect: "Collaborate on readings, publications, education programmes or diaspora events.",
  },
  {
    id: "craft",
    name: "Craft & Cultural Practice",
    icon: "◈",
    meaning: "Skills learned by making: objects, techniques, materials and the knowledge around them.",
    people: "Makers, artisans, practitioners of everyday and ceremonial crafts, and teachers of making.",
    preserve: "Process notes, material knowledge, photographs of work, and respect for designs that should not be copied.",
    upload: "Photo/craft items, project notes, workshop offers, and documentation of technique (text and filenames).",
    participate: "Show practice in a public profile, list workshops, or share notes with consent.",
    connect: "Museum programmes, training, community projects and research — with consent and attribution.",
  },
  {
    id: "diaspora",
    name: "Diaspora Connection",
    icon: "◎",
    meaning: "How Rwandans abroad stay linked to language, ceremony, stories and people at home.",
    people: "Diaspora families, cultural groups overseas, visitors, and practitioners in Rwanda who welcome exchange.",
    preserve: "Migration stories, language practice abroad, event records, and links between home and host communities.",
    upload: "Diaspora stories, event documentation, interviews, and collaboration notes (no private addresses).",
    participate: "Share a diaspora story, list availability for diaspora events, or follow practitioners in Rwanda.",
    connect: "Bridge requests for teaching, performances, research or community documentation across countries.",
  },
];

const AVAIL_OPTIONS = [
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
];

const PORTFOLIO_TYPES = [
  "Video / Performance",
  "Audio / Song",
  "Written Story",
  "Poetry",
  "Photo / Craft",
  "Interview / Oral History",
  "Project",
  "Workshop",
  "Cultural documentation",
];

const COLLAB_TYPES = [
  "Performance",
  "Workshop",
  "Interview",
  "Research",
  "School Visit",
  "Mentorship",
  "Event",
];

function read(k) {
  return JSON.parse(localStorage.getItem(k) || "[]");
}
function write(k, v) {
  localStorage.setItem(k, JSON.stringify(v));
}
function uid(p) {
  return p + "-" + Date.now() + "-" + Math.random().toString(36).slice(2, 7);
}
function qs(s) {
  return document.querySelector(s);
}
function esc(v) {
  return String(v || "").replace(/[&<>"']/g, (m) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[m]));
}
function currentUser() {
  return JSON.parse(localStorage.getItem(DB.session) || "null");
}
function setSession(u) {
  localStorage.setItem(DB.session, JSON.stringify({ id: u.id, name: u.name, email: u.email, role: u.role }));
}
function logout() {
  localStorage.removeItem(DB.session);
  location.href = "index.html";
}
function requireAuth(role) {
  const u = currentUser();
  if (!u) {
    location.href = "login.html";
    return null;
  }
  if (role && u.role !== role) {
    location.href = u.role === "admin" ? "admin.html" : "dashboard.html";
    return null;
  }
  return u;
}
function statusBadge(s) {
  return `<span class="badge ${String(s).toLowerCase()}">${esc(s)}</span>`;
}
function initials(name) {
  return String(name || "?")
    .split(/\s+/)
    .slice(0, 2)
    .map((p) => p[0])
    .join("")
    .toUpperCase();
}
function param(name) {
  return new URLSearchParams(location.search).get(name);
}
function areaById(id) {
  return localizedAreas().find((a) => a.id === id) || localizedAreas()[0];
}
function currentLang() {
  return localStorage.getItem("up2_lang") || "en";
}
function tr(key) {
  const pack = (typeof I18N !== "undefined" && (I18N[currentLang()] || I18N.en)) || {};
  return pack[key] || (I18N && I18N.en[key]) || key;
}
function localizedAreas() {
  const pack = (typeof AREA_I18N !== "undefined" && (AREA_I18N[currentLang()] || AREA_I18N.en)) || {};
  return AREAS.map((a) => Object.assign({}, a, pack[a.id] || {}));
}

function seed() {
  if (!localStorage.getItem(DB.users)) {
    write(DB.users, [
      {
        id: "admin-1",
        name: "UmucoPulse Administrator",
        email: "admin@umucopulse.org",
        password: "Umuco123!",
        role: "admin",
      },
      {
        id: "contributor-1",
        name: "Sylvie Umutoni Rutaganira",
        email: "sylvie@umucopulse.org",
        password: "Story123!",
        role: "contributor",
      },
    ]);
  }
  const users = read(DB.users);
  const sylvie = users.find((u) => u.email === "sylvie@umucopulse.org");
  const aline = users.find((u) => u.email === "aline@umucopulse.org");
  if (aline && !sylvie) {
    aline.email = "sylvie@umucopulse.org";
    aline.name = "Sylvie Umutoni Rutaganira";
    aline.password = "Story123!";
    write(DB.users, users);
  } else if (!sylvie) {
    users.push({
      id: "contributor-1",
      name: "Sylvie Umutoni Rutaganira",
      email: "sylvie@umucopulse.org",
      password: "Story123!",
      role: "contributor",
    });
    write(DB.users, users);
  } else if (sylvie.name !== "Sylvie Umutoni Rutaganira") {
    sylvie.name = "Sylvie Umutoni Rutaganira";
    write(DB.users, users);
  }
  if (!localStorage.getItem(DB.projects)) {
    write(DB.projects, [
      {
        id: "p1",
        title: "Heritage Workshops",
        category: "education",
        description: "Example project: a school or centre could list workshops here. This is not a running programme.",
      },
      {
        id: "p2",
        title: "Voices Archive",
        category: "archive",
        description: "Example project for keeping stories and recordings after consent. Not a national archive.",
      },
      {
        id: "p3",
        title: "Performances & Gatherings",
        category: "performance",
        description: "Example project for a public sharing. Not a ticketed tour and not a confirmed booking.",
      },
    ]);
  }
  if (!localStorage.getItem(DB.submissions)) {
    write(DB.submissions, [
      {
        id: "seed-1",
        userId: "seed",
        contributor: "Community Voice",
        email: "hidden",
        title: "A family story (demo)",
        type: "Written Story",
        category: "Community Story",
        story:
          "This is a sample card. A real story would be written by the person who shared it, after consent and review.",
        mediaName: "No media attached",
        consent: true,
        status: "Published",
        feedback: "",
        submittedAt: "2026-08-08T08:00:00Z",
        publishedAt: "2026-08-10T08:00:00Z",
        demo: true,
      },
      {
        id: "seed-2",
        userId: "seed",
        contributor: "Young Cultural Practitioner",
        email: "hidden",
        title: "A dance note (demo)",
        type: "Dance / Performance",
        category: "Dance",
        story:
          "This is a sample card. A dancer would write here in their own words. It is not a real performance report.",
        mediaName: "performance-demo.mp4",
        consent: true,
        status: "Published",
        feedback: "",
        submittedAt: "2026-08-11T08:00:00Z",
        publishedAt: "2026-08-12T08:00:00Z",
        demo: true,
      },
    ]);
  }
  if (!localStorage.getItem(DB.contacts)) write(DB.contacts, []);
  if (!localStorage.getItem(DB.subscribers)) write(DB.subscribers, []);
  if (!localStorage.getItem(DB.follows)) write(DB.follows, []);
  if (!localStorage.getItem(DB.collabs)) write(DB.collabs, []);
  if (!localStorage.getItem(DB.profiles)) {
    const demos = [
      {
        id: "prof-inyamibwa",
        userId: "org-inyamibwa",
        displayName: "Inyamibwa Cultural Troupe (ICT)",
        area: "dance",
        kind: "troupe",
        role: "Cultural Organisation",
        location: "Kigali",
        languages: "",
        bio: "Music and dance focused on unity and healing.",
        background: "Founded in 1998.",
        communityNote: "Over 100 members.",
        skills: "Music, dance",
        available: [],
        website: "",
        photo: "",
        isPublic: true,
        curated: true,
        isDemo: false,
      },
      {
        id: "prof-inganzo",
        userId: "org-inganzo",
        displayName: "Inganzo Ngari",
        area: "dance",
        kind: "troupe",
        role: "Cultural Organisation",
        location: "",
        languages: "",
        bio: "Traditional dance and folkloric group with strong youth and international visibility.",
        background: "Formed in 2006.",
        communityNote: "",
        skills: "Traditional dance, folklore",
        available: [],
        website: "",
        photo: "",
        isPublic: true,
        curated: true,
        isDemo: false,
      },
      {
        id: "prof-intayoberana",
        userId: "org-intayoberana",
        displayName: "Intayoberana Cultural Troupe",
        area: "dance",
        kind: "troupe",
        role: "Cultural Organisation",
        location: "",
        languages: "",
        bio: "Traditional Rwandan cultural troupe",
        background: "",
        communityNote: "Includes the children's cultural group Uruyange.",
        skills: "Intore, Umushagiriro, Ikinimba",
        available: [],
        website: "",
        photo: "",
        isPublic: true,
        curated: true,
        isDemo: false,
      },
      {
        id: "prof-indinzi",
        userId: "org-indinzi",
        displayName: "Indinzi Cultural Troupe",
        area: "dance",
        kind: "troupe",
        role: "Cultural Organisation",
        location: "",
        languages: "",
        bio: "Combines dance, drumming, storytelling and community teaching.",
        background: "",
        communityNote: "",
        skills: "Dance, drumming, storytelling, community teaching",
        available: [],
        website: "",
        photo: "",
        isPublic: true,
        curated: true,
        isDemo: false,
      },
      {
        id: "prof-demo-oral",
        userId: "demo-oral",
        displayName: "Demo Memory Keeper",
        area: "oral",
        kind: "individual",
        role: "Oral historian (prototype)",
        location: "Huye, Rwanda",
        languages: "Kinyarwanda, French",
        bio: "Illustrative profile for recording family and community testimony with consent.",
        background: "Demo content. Not a real person.",
        skills: "Interviewing, transcription notes, community listening",
        available: ["interviews", "cultural research", "community projects"],
        isPublic: true,
        curated: false,
        isDemo: true,
      },
      {
        id: "prof-demo-music",
        userId: "demo-music",
        displayName: "Demo Inanga Circle",
        area: "music",
        kind: "community_group",
        role: "Musicians and song keepers",
        location: "Musanze, Rwanda",
        languages: "Kinyarwanda, English",
        bio: "Prototype musicians showing how song meaning and performance notes can live beside a profile.",
        background: "Fictional ensemble for the GitHub Pages prototype.",
        skills: "Song, accompaniment, cultural explanation",
        available: ["performances", "workshops", "diaspora events"],
        isPublic: true,
        curated: true,
        isDemo: true,
      },
      {
        id: "prof-demo-poetry",
        userId: "demo-poetry",
        displayName: "Demo Spoken Word Studio",
        area: "poetry",
        kind: "community_group",
        role: "Poets and storytellers",
        location: "Kigali, Rwanda",
        languages: "Kinyarwanda, English, French",
        bio: "Example writers documenting poems and storytelling for learners and community stages.",
        background: "Demo identity for Poetry & Storytelling.",
        skills: "Spoken word, classroom storytelling, bilingual performance",
        available: ["school visits", "mentorship", "festivals", "collaborations"],
        isPublic: true,
        curated: false,
        isDemo: true,
      },
      {
        id: "prof-demo-craft",
        userId: "demo-craft",
        displayName: "Demo Agaseke Practice",
        area: "craft",
        kind: "individual",
        role: "Craft practitioners",
        location: "Nyamata, Rwanda",
        languages: "Kinyarwanda",
        bio: "Illustrative makers profile: process, materials and teaching — not a real workshop brand.",
        background: "Prototype content for Craft & Cultural Practice.",
        skills: "Weaving knowledge, making demonstrations, documentation",
        available: ["workshops", "museum programmes", "community projects"],
        isPublic: true,
        curated: false,
        isDemo: true,
      },
      {
        id: "prof-demo-diaspora",
        userId: "demo-diaspora",
        displayName: "Demo Diaspora Circle",
        area: "diaspora",
        kind: "community_group",
        role: "Diaspora cultural organisers",
        location: "Mauritius (demo location)",
        languages: "English, French, Kinyarwanda",
        bio: "Fictional diaspora group showing how people abroad can connect with practitioners in Rwanda.",
        background: "Demo only. No real organisation is claimed.",
        skills: "Event hosting, language practice, cultural exchange",
        available: ["diaspora events", "collaborations", "community projects"],
        isPublic: true,
        curated: false,
        isDemo: true,
      },
      {
        id: "prof-sylvie",
        userId: "founder-sylvie",
        displayName: "Umutoni Rutaganira Sylvie",
        area: "poetry",
        kind: "individual",
        role: "Founder of UmucoPulse",
        location: "",
        languages: "",
        bio: "Started UmucoPulse as a student project for community cultural heritage. The platform is for the community, not a personal portfolio.",
        background: "",
        communityNote: "",
        skills: "",
        available: [],
        website: "",
        photo: "",
        isPublic: true,
        curated: true,
        isDemo: false,
      },
    ];
    write(DB.profiles, demos);
    write(DB.portfolio, [
      {
        id: "port-intayo-1",
        profileId: "prof-intayoberana",
        title: "Traditional dance performances",
        type: "Performance",
        description: "",
        context: "",
        link: "",
        date: "",
        mediaName: "",
      },
      {
        id: "port-intayo-2",
        profileId: "prof-intayoberana",
        title: "Intore performances",
        type: "Performance",
        description: "",
        context: "",
        link: "",
        date: "",
        mediaName: "",
      },
      {
        id: "port-intayo-3",
        profileId: "prof-intayoberana",
        title: "Umushagiriro performances",
        type: "Performance",
        description: "",
        context: "",
        link: "",
        date: "",
        mediaName: "",
      },
      {
        id: "port-intayo-4",
        profileId: "prof-intayoberana",
        title: "Ikinimba performances",
        type: "Performance",
        description: "",
        context: "",
        link: "",
        date: "",
        mediaName: "",
      },
      {
        id: "port-intayo-5",
        profileId: "prof-intayoberana",
        title: "Youth/children's cultural performances",
        type: "Performance",
        description: "",
        context: "",
        link: "",
        date: "",
        mediaName: "",
      },
      {
        id: "port-2",
        profileId: "prof-demo-oral",
        title: "Listening session outline (demo)",
        type: "Interview / Oral History",
        description: "How consent and context can sit next to an interview record.",
        context: "Demo documentation, not a real elder interview.",
        link: "",
        date: "2026-05-12",
        mediaName: "demo-interview.m4a",
      },
      {
        id: "port-3",
        profileId: "prof-demo-music",
        title: "Song meaning notes (demo)",
        type: "Audio / Song",
        description: "Short cultural explanation stored as text in the prototype.",
        context: "Illustrative song notes.",
        link: "",
        date: "2026-04-20",
        mediaName: "demo-song.mp3",
      },
    ]);
  }
  if (!localStorage.getItem(DB.opportunities)) {
    write(DB.opportunities, [
      {
        id: "opp-1",
        title: "School cultural exchange session",
        category: "school programmes",
        location: "Open (prototype)",
        description: "Illustrative call for practitioners willing to visit a classroom. Not a real school booking.",
        isDemo: true,
      },
      {
        id: "opp-2",
        title: "Community documentation weekend",
        category: "community projects",
        location: "Rwanda (prototype)",
        description: "Example of how a neighbourhood might invite oral historians. Demo listing only.",
        isDemo: true,
      },
      {
        id: "opp-3",
        title: "Diaspora storytelling evening",
        category: "diaspora programmes",
        location: "Online / host city (prototype)",
        description: "Fictional gathering format for connecting diaspora listeners with practitioners. Not an official event.",
        isDemo: true,
      },
      {
        id: "opp-4",
        title: "Museum learning workshop (illustrative)",
        category: "museum opportunities",
        location: "To be confirmed",
        description: "Shows how a cultural institution could later post a call. No partnership is claimed.",
        isDemo: true,
      },
    ]);
  }
  if (!localStorage.getItem(DB.events)) {
    write(DB.events, [
      {
        id: "ev-1",
        title: "Traditional dance sharing (illustrative listing)",
        type: "performance",
        hostId: "prof-intayoberana",
        location: "Kigali",
        date: "Prototype example",
        description: "An example of how Intayoberana could list a public sharing. Not a confirmed real-world booking.",
        isDemo: true,
      },
      {
        id: "ev-2",
        title: "Community music and dance for unity (illustrative listing)",
        type: "gathering",
        hostId: "prof-inyamibwa",
        location: "Kigali",
        date: "Prototype example",
        description: "Example gathering format. Not a ticketed event claim.",
        isDemo: true,
      },
      {
        id: "ev-3",
        title: "Classroom oral-history listening session (demo)",
        type: "workshop",
        hostId: "prof-demo-oral",
        location: "Huye",
        date: "Prototype example",
        description: "Demo workshop for consent-based documentation.",
        isDemo: true,
      },
      {
        id: "ev-4",
        title: "Virtual diaspora cultural evening (demo)",
        type: "gathering",
        hostId: "prof-demo-diaspora",
        location: "Online / host city",
        date: "Prototype example",
        description: "Example diaspora gathering. Not an official programme.",
        isDemo: true,
      },
    ]);
  }
  if (!localStorage.getItem(DB.library)) {
    write(DB.library, [
      {
        id: "lib-1",
        title: "Intore teaching notes (prototype booklet)",
        type: "Booklet",
        area: "dance",
        author: "UmucoPulse archive (demo)",
        visibility: "public",
        status: "published",
        fileName: "intore-notes-example.pdf",
        description: "Illustrative booklet record. File name only.",
      },
    ]);
  }
  patchDemoCopy();
  migrateProfiles();
}

function patchDemoCopy() {
  const projects = read(DB.projects);
  const projectText = {
    p1: "Example project: a school or centre could list workshops here. This is not a running programme.",
    p2: "Example project for keeping stories and recordings after consent. Not a national archive.",
    p3: "Example project for a public sharing. Not a ticketed tour and not a confirmed booking.",
  };
  let changed = false;
  projects.forEach((p) => {
    if (projectText[p.id] && p.description !== projectText[p.id]) {
      p.description = projectText[p.id];
      changed = true;
    }
  });
  if (changed) write(DB.projects, projects);
  const stories = read(DB.submissions);
  const storyText = {
    "seed-1": {
      title: "A family story (demo)",
      story: "This is a sample card. A real story would be written by the person who shared it, after consent and review.",
    },
    "seed-2": {
      title: "A dance note (demo)",
      story: "This is a sample card. A dancer would write here in their own words. It is not a real performance report.",
    },
  };
  let storyChanged = false;
  stories.forEach((s) => {
    const next = storyText[s.id];
    if (next && (s.title !== next.title || s.story !== next.story)) {
      s.title = next.title;
      s.story = next.story;
      storyChanged = true;
    }
  });
  if (storyChanged) write(DB.submissions, stories);
}

function danceTroupes() {
  return [
    {
      id: "prof-inyamibwa",
      userId: "org-inyamibwa",
      displayName: "Inyamibwa Cultural Troupe (ICT)",
      area: "dance",
      kind: "troupe",
      role: "Cultural Organisation",
      location: "Kigali",
      languages: "",
      bio: "Music and dance focused on unity and healing.",
      background: "Founded in 1998.",
      communityNote: "Over 100 members.",
      skills: "Music, dance",
      available: [],
      website: "",
      photo: "",
      isPublic: true,
      curated: true,
      isDemo: false,
    },
    {
      id: "prof-inganzo",
      userId: "org-inganzo",
      displayName: "Inganzo Ngari",
      area: "dance",
      kind: "troupe",
      role: "Cultural Organisation",
      location: "",
      languages: "",
      bio: "Traditional dance and folkloric group with strong youth and international visibility.",
      background: "Formed in 2006.",
      communityNote: "",
      skills: "Traditional dance, folklore",
      available: [],
      website: "",
      photo: "",
      isPublic: true,
      curated: true,
      isDemo: false,
    },
    {
      id: "prof-intayoberana",
      userId: "org-intayoberana",
      displayName: "Intayoberana Cultural Troupe",
      area: "dance",
      kind: "troupe",
      role: "Cultural Organisation",
      location: "",
      languages: "",
      bio: "Traditional Rwandan cultural troupe",
      background: "",
      communityNote: "Includes the children's cultural group Uruyange.",
      skills: "Intore, Umushagiriro, Ikinimba",
      available: [],
      website: "",
      photo: "",
      isPublic: true,
      curated: true,
      isDemo: false,
    },
    {
      id: "prof-indinzi",
      userId: "org-indinzi",
      displayName: "Indinzi Cultural Troupe",
      area: "dance",
      kind: "troupe",
      role: "Cultural Organisation",
      location: "",
      languages: "",
      bio: "Combines dance, drumming, storytelling and community teaching.",
      background: "",
      communityNote: "",
      skills: "Dance, drumming, storytelling, community teaching",
      available: [],
      website: "",
      photo: "",
      isPublic: true,
      curated: true,
      isDemo: false,
    },
  ];
}

function migrateProfiles() {
  if (!localStorage.getItem(DB.profiles)) return;
  let list = read(DB.profiles);
  list = list.filter((p) => p.id !== "prof-demo-dance" && p.displayName !== "Demo Intore Ensemble");
  const kinds = {
    "prof-demo-oral": "individual",
    "prof-demo-music": "community_group",
    "prof-demo-poetry": "community_group",
    "prof-demo-craft": "individual",
    "prof-demo-diaspora": "community_group",
  };
  list.forEach((p) => {
    if (!p.kind) p.kind = kinds[p.id] || (p.area === "dance" ? "troupe" : "individual");
    if (!Array.isArray(p.available)) p.available = p.available ? String(p.available).split("|") : [];
    if (p.website == null) p.website = "";
    if (p.photo == null) p.photo = "";
    if (p.communityNote == null) p.communityNote = "";
  });
  danceTroupes().forEach((troupe) => {
    const i = list.findIndex((p) => p.id === troupe.id || p.displayName === troupe.displayName);
    if (i >= 0) list[i] = Object.assign({}, list[i], troupe);
    else list.push(troupe);
  });
  write(DB.profiles, list);
  let port = read(DB.portfolio) || [];
  port = port.filter((w) => w.profileId !== "prof-demo-dance");
  [
    ["port-intayo-1", "Traditional dance performances"],
    ["port-intayo-2", "Intore performances"],
    ["port-intayo-3", "Umushagiriro performances"],
    ["port-intayo-4", "Ikinimba performances"],
    ["port-intayo-5", "Youth/children's cultural performances"],
  ].forEach(([id, title]) => {
    if (!port.find((w) => w.id === id)) {
      port.push({ id, profileId: "prof-intayoberana", title, type: "Performance", description: "", context: "", link: "", date: "", mediaName: "" });
    }
  });
  write(DB.portfolio, port);
  upsertFounderProfile();
}

function founderProfile() {
  return {
    id: "prof-sylvie",
    userId: "founder-sylvie",
    displayName: "Umutoni Rutaganira Sylvie",
    area: "poetry",
    kind: "individual",
    role: "Founder of UmucoPulse",
    location: "",
    languages: "",
    bio: "Started UmucoPulse as a student project for community cultural heritage. The platform is for the community, not a personal portfolio.",
    background: "",
    communityNote: "",
    skills: "",
    available: [],
    website: "",
    photo: "",
    isPublic: true,
    curated: true,
    isDemo: false,
  };
}

function upsertFounderProfile() {
  if (!localStorage.getItem(DB.profiles)) return;
  const list = read(DB.profiles);
  const founder = founderProfile();
  const i = list.findIndex(
    (p) =>
      p.id === founder.id ||
      p.displayName === founder.displayName ||
      p.displayName === "Sylvie Umutoni Rutaganira"
  );
  if (i >= 0) list[i] = Object.assign({}, list[i], founder);
  else list.push(founder);
  write(DB.profiles, list);
}

function fillNav() {
  const nav = qs("[data-nav]");
  if (!nav) return;
  const file = (location.pathname.split("/").pop() || "index.html").split("?")[0] || "index.html";
  const discoverFiles = ["discover.html", "events.html", "knowledge.html", "learn.html", "diaspora.html", "articles.html", "article-impact.html"];
  const links = [
    ["index.html", tr("home")],
    ["discover.html", tr("discover")],
    ["creators.html", tr("creators")],
    ["voice.html", tr("voices")],
    ["opportunities.html", tr("opportunities")],
    ["about.html", tr("about")],
  ];
  const lang = currentLang();
  const u = currentUser();
  let auth = "";
  if (u && u.role === "admin") {
    auth = `<details class="account-menu"><summary class="account-chip" title="${esc(u.name)}"><span class="nav-avatar" aria-hidden="true">${esc((u.name || "U").charAt(0).toUpperCase())}</span><span class="sr-only">${esc(u.name.split(" ")[0])}</span></summary><div class="account-panel">
      <a href="admin.html">${tr("dashboard")}</a>
      <a href="admin.html#stories">${tr("admin_submissions")}</a>
      <a href="admin.html#creators-admin">${tr("creators")}</a>
      <a href="admin.html#projects-admin">${tr("projects")}</a>
      <a href="admin.html#contacts-admin">${tr("admin_messages")}</a>
      <a href="#" id="logout-link">${tr("logout")}</a></div></details>`;
  } else if (u) {
    auth = `<details class="account-menu"><summary class="account-chip" title="${esc(u.name)}"><span class="nav-avatar" aria-hidden="true">${esc((u.name || "U").charAt(0).toUpperCase())}</span><span class="sr-only">${esc(u.name.split(" ")[0])}</span></summary><div class="account-panel">
      <a href="dashboard.html">${tr("dashboard")}</a>
      <a href="profile.html">${tr("my_profile")}</a>
      <a href="profile.html#portfolio">${tr("my_portfolio")}</a>
      <a href="dashboard.html#stories">${tr("my_stories")}</a>
      <a href="dashboard.html#connections">${tr("connections")}</a>
      <a href="saved.html">${tr("saved_items")}</a>
      <a href="#" id="logout-link">${tr("logout")}</a></div></details>`;
  } else {
    auth = `<a href="login.html">${tr("login")}</a><a class="btn small clay" href="register.html">${tr("join")}</a>`;
  }
  nav.innerHTML =
    links
      .map(([h, l]) => {
        const active = file === h || (h === "discover.html" && discoverFiles.includes(file));
        return `<a href="${h}" class="${active ? "active" : ""}">${l}</a>`;
      })
      .join("") +
    `<select id="language" class="lang" aria-label="${tr("lang")}"><option value="en">EN</option><option value="rw">RW</option><option value="fr">FR</option></select>`;
  let end = qs(".nav-end");
  if (!end && nav.parentElement) {
    end = document.createElement("div");
    end.className = "nav-end";
    nav.after(end);
  }
  if (end) end.innerHTML = auth;
  const sel = qs("#language");
  if (sel) {
    sel.value = lang;
    sel.onchange = (e) => applyLanguage(e.target.value);
  }
  const lo = qs("#logout-link");
  if (lo)
    lo.onclick = (e) => {
      e.preventDefault();
      logout();
    };
}

function applyLanguage(lang) {
  if (lang) localStorage.setItem("up2_lang", lang);
  lang = currentLang();
  document.documentElement.lang = lang === "rw" ? "rw" : lang;
  const dict = (typeof I18N !== "undefined" && (I18N[lang] || I18N.en)) || {};
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const k = el.getAttribute("data-i18n");
    if (dict[k] != null) el.textContent = dict[k];
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const k = el.getAttribute("data-i18n-placeholder");
    if (dict[k] != null) el.placeholder = dict[k];
  });
  fillNav();
  if (qs("#home-areas") || qs("#impact-stats") || qs("#featured-group")) renderHomeExtras();
  if (qs("#discover-areas")) renderDiscover();
  if (qs("#creators-grid")) renderCreators();
  if (qs("#event-grid")) renderEvents();
  if (qs("#creator-profile")) renderCreator();
  if (qs("#opp-grid")) renderOpportunities();
  if (qs("#community-stories")) renderVoices();
  if (qs("#projects-grid")) renderProjects();
  if (qs("#submission-list") || qs("#welcome")) {
    try {
      renderDashboard();
    } catch (e) {}
  }
}

document.addEventListener("DOMContentLoaded", () => {
  seed();
  fillNav();
  applyLanguage(localStorage.getItem("up2_lang") || "en");
  const news = qs("#newsletter-form");
  if (news)
    news.onsubmit = (e) => {
      e.preventDefault();
      const a = read(DB.subscribers);
      const email = qs("#newsletter-email").value.trim().toLowerCase();
      if (email && !a.includes(email)) {
        a.push(email);
        write(DB.subscribers, a);
      }
      qs("#newsletter-result").innerHTML = '<span class="success-text">' + tr("subscribed") + "</span>";
      news.reset();
    };
});

function registerUser(e) {
  e.preventDefault();
  const users = read(DB.users);
  const email = qs("#email").value.trim().toLowerCase();
  const out = qs("#form-result");
  if (users.some((u) => u.email === email)) {
    out.innerHTML = '<span class="error">An account with this email already exists.</span>';
    return;
  }
  const password = qs("#password").value;
  if (password.length < 6) {
    out.innerHTML = '<span class="error">Password must have at least 6 characters.</span>';
    return;
  }
  const u = { id: uid("user"), name: qs("#name").value.trim(), email, password, role: "contributor" };
  users.push(u);
  write(DB.users, users);
  const profiles = read(DB.profiles);
  profiles.push({
    id: uid("prof"),
    userId: u.id,
    displayName: u.name,
    area: "oral",
    kind: "individual",
    role: "",
    location: "",
    languages: "",
    bio: "",
    background: "",
    skills: "",
    available: [],
    isPublic: false,
    curated: false,
    isDemo: false,
  });
  write(DB.profiles, profiles);
  setSession(u);
  location.href = "profile.html";
}

function loginUser(e) {
  e.preventDefault();
  const email = qs("#email").value.trim().toLowerCase();
  const password = qs("#password").value;
  const u = read(DB.users).find((x) => x.email === email && x.password === password);
  if (!u) {
    qs("#form-result").innerHTML = '<span class="error">Incorrect email or password.</span>';
    return;
  }
  setSession(u);
  location.href = u.role === "admin" ? "admin.html" : "dashboard.html";
}

function submitStory(e) {
  e.preventDefault();
  const u = requireAuth("contributor");
  if (!u) return;
  if (!qs("#consent").checked) {
    qs("#form-result").innerHTML = '<span class="error">Consent is required before submission.</span>';
    return;
  }
  const f = qs("#media") && qs("#media").files[0];
  const x = {
    id: uid("story"),
    userId: u.id,
    contributor: u.name,
    email: u.email,
    title: qs("#title").value.trim(),
    type: qs("#type").value,
    category: qs("#category") ? qs("#category").value : "Community Story",
    story: qs("#story").value.trim(),
    mediaName: f ? f.name : "No media attached",
    consent: true,
    status: "Pending",
    feedback: "",
    submittedAt: new Date().toISOString(),
    publishedAt: null,
    demo: false,
  };
  const a = read(DB.submissions);
  a.unshift(x);
  write(DB.submissions, a);
  qs("#form-result").innerHTML = '<span class="success-text">Story submitted for review.</span>';
  e.target.reset();
  setTimeout(() => (location.href = "dashboard.html"), 500);
}

function myProfile(userId) {
  return read(DB.profiles).find((p) => p.userId === userId);
}
function profileById(id) {
  return read(DB.profiles).find((p) => p.id === id);
}
function portfolioFor(profileId) {
  return read(DB.portfolio).filter((i) => i.profileId === profileId);
}
function followerCount(profileId) {
  return read(DB.follows).filter((f) => f.creatorId === profileId).length;
}
function isFollowing(profileId) {
  const u = currentUser();
  if (!u) return false;
  return read(DB.follows).some((f) => f.followerId === u.id && f.creatorId === profileId);
}

function toggleFollow(profileId) {
  const u = currentUser();
  if (!u) {
    location.href = "login.html";
    return;
  }
  const mine = myProfile(u.id);
  if (mine && mine.id === profileId) return;
  let a = read(DB.follows);
  if (isFollowing(profileId)) a = a.filter((f) => !(f.followerId === u.id && f.creatorId === profileId));
  else a.push({ id: uid("fol"), followerId: u.id, creatorId: profileId, at: new Date().toISOString() });
  write(DB.follows, a);
  if (typeof renderCreator === "function" && qs("#creator-profile")) renderCreator();
  if (typeof renderCreators === "function" && qs("#creators-grid")) renderCreators();
}

function publicProfiles() {
  return read(DB.profiles).filter((p) => p.isPublic);
}

function kindLabel(kind) {
  if (kind === "troupe") return tr("kind_org");
  if (kind === "community_group") return tr("kind_community");
  if (kind === "individual") return tr("kind_individual");
  return tr("practitioner");
}

function practicesList(p) {
  return String(p.skills || "")
    .split(/[·|,]/)
    .map((x) => x.trim())
    .filter(Boolean);
}

function langTokens(text) {
  return String(text || "")
    .replace(/[·|;/]/g, ",")
    .split(",")
    .map((x) => x.trim().toLowerCase())
    .filter(Boolean);
}

function trFill(key, vars) {
  let out = tr(key);
  Object.keys(vars || {}).forEach((k) => {
    out = out.replace("{" + k + "}", vars[k]);
  });
  return out;
}

function similarProfiles(source, youBoth) {
  if (!source) return [];
  const u = currentUser();
  const mine = u ? myProfile(u.id) : null;
  const srcPractices = new Set(practicesList(source).map((x) => x.toLowerCase()));
  const srcLangs = new Set(langTokens(source.languages));
  const srcLoc = locKey(source);
  return publicProfiles()
    .map((p) => {
      if (p.id === source.id) return null;
      if (mine && p.id === mine.id) return null;
      let score = 0;
      const reasons = [];
      const area = areaById(source.area);
      if (source.area && p.area === source.area) {
        score += 4;
        reasons.push(trFill(youBoth ? "same_art_area" : "same_art_area_also", { area: area.name }));
      }
      const sharedP = practicesList(p).map((x) => x.toLowerCase()).filter((x) => srcPractices.has(x));
      if (sharedP.length) {
        score += 2 * Math.min(sharedP.length, 3);
        reasons.push(trFill("same_art_practice", { practice: sharedP[0] }));
      }
      const pLoc = locKey(p);
      if (srcLoc && srcLoc !== "unlisted" && pLoc === srcLoc) {
        score += 2;
        reasons.push(trFill("same_art_place", { place: p.location || srcLoc }));
      }
      const sharedL = langTokens(p.languages).filter((x) => srcLangs.has(x));
      if (sharedL.length) {
        score += 1;
        reasons.push(trFill("same_art_lang", { lang: sharedL[0] }));
      }
      if (!score) return null;
      return { profile: p, score, reason: reasons[0] || tr("same_art_generic") };
    })
    .filter(Boolean)
    .sort((a, b) => b.score - a.score || a.profile.displayName.localeCompare(b.profile.displayName))
    .slice(0, 5);
}

function renderMeetArt(source, youBoth) {
  const root = qs("#meet-art");
  if (!root) return;
  const rows = similarProfiles(source, youBoth);
  if (!rows.length) {
    root.innerHTML = "";
    return;
  }
  const u = currentUser();
  root.innerHTML = `<h2>${tr("meet_same_art")}</h2><p class="help">${tr("meet_same_art_lead")}</p>
    <div class="grid">${rows
      .map((item) => {
        const p = item.profile;
        const connect = u
          ? `<a class="btn small" href="creator.html?id=${encodeURIComponent(p.id)}#collab">${tr("connect_cta")}</a>`
          : `<a class="btn small" href="login.html">${tr("connect_cta")}</a>`;
        return `<article class="card rec-card">
          <p class="tag">${esc(areaById(p.area).name)}</p>
          <h3>${esc(p.displayName)}</h3>
          <p class="story-meta">${esc(kindLabel(p.kind))}${p.location ? " · " + esc(p.location) : ""}</p>
          <p class="help">${esc(item.reason)}</p>
          <div class="actions">
            <a class="btn small blue" href="creator.html?id=${encodeURIComponent(p.id)}">${tr("view_profile")}</a>
            ${connect}
          </div>
        </article>`;
      })
      .join("")}</div>`;
}

function avatarHtml(p, extra) {
  const ready = !p.photo && (p.kind === "troupe" || p.kind === "community_group") ? " photo-ready" : "";
  const photo = p.photo ? " has-photo" : "";
  if (p.photo) return `<div class="avatar ${extra || ""}${photo}"><img src="${esc(p.photo)}" alt=""></div>`;
  return `<div class="avatar ${extra || ""}${ready}" aria-hidden="true">${esc(initials(p.displayName))}</div>`;
}

function creatorCard(p) {
  const works = portfolioFor(p.id).length;
  const area = areaById(p.area);
  const followLabel = isFollowing(p.id) ? tr("following") : tr("follow");
  const kindTag =
    p.kind === "troupe"
      ? `<span class="tag">${tr("kind_troupe_one")}</span>`
      : p.kind === "community_group"
        ? `<span class="tag">${tr("kind_community")}</span>`
        : p.kind === "organisation"
          ? `<span class="tag">${tr("kind_organisation")}</span>`
          : `<span class="tag">${tr("kind_individual")}</span>`;
  const practices = practicesList(p);
  const website = p.website
    ? `<a class="btn ghost small" href="${esc(p.website)}" rel="noopener noreferrer" target="_blank">${tr("visit_website")}</a>`
    : "";
  return `<article class="card creator-card">
    ${avatarHtml(p)}
    <div class="creator-tags">    ${p.isDemo ? `<span class="tag demo-tag">${tr("demo_profile")}</span>` : ""} ${kindTag} ${p.curated ? `<span class="tag curated">${tr("reviewed")}</span>` : ""}</div>
    <h3>${esc(p.displayName)}</h3>
    <p class="story-meta">${esc(p.kind === "troupe" ? tr("kind_troupe_one") : p.kind === "organisation" ? tr("kind_organisation") : p.role || tr("practitioner"))} · ${esc(area.name)}</p>
    ${p.location ? `<p class="story-meta">${esc(p.location)}</p>` : ""}
    <p>${esc((p.bio || "").slice(0, 140))}${(p.bio || "").length > 140 ? "…" : ""}</p>
    ${practices.length ? `<p class="story-meta">${tr("practices")}: ${esc(practices.join(" · "))}</p>` : ""}
    <p class="story-meta">${works} ${tr("works")} · ${followerCount(p.id)} ${tr("followers")}</p>
    <div class="actions">
      <a class="btn small" href="creator.html?id=${encodeURIComponent(p.id)}">${tr("view_profile")}</a>
      <button class="btn ghost small" type="button" onclick="toggleFollow('${p.id}')">${followLabel}</button>
      <a class="btn ghost small" href="creator.html?id=${encodeURIComponent(p.id)}">${tr("request_collab")}</a>
      ${website}
    </div>
  </article>`;
}

function renderHomeExtras() {
  const areas = qs("#home-areas");
  if (areas)
    areas.innerHTML = localizedAreas()
      .map(
        (a) => `<article class="card"><div class="icon">${a.icon}</div><h3>${esc(a.name)}</h3><p>${esc(a.meaning)}</p><a href="discover.html#${a.id}"><strong>${tr("explore_arrow")}</strong></a></article>`
      )
      .join("");
  const feat = qs("#featured-creators");
  if (feat) {
    const featured = publicProfiles()
      .slice()
      .sort((a, b) => Number(!!b.curated) - Number(!!a.curated))
      .slice(0, 3);
    feat.innerHTML = featured.map(creatorCard).join("");
  }
  const stories = qs("#featured-stories");
  if (stories) {
    const pub = read(DB.submissions).filter((x) => x.status === "Published").slice(0, 3);
    stories.innerHTML = pub
      .map(
        (x) => `<article class="card story-card"><span class="tag">${esc(x.category || x.type)}</span><h3>${esc(x.title)}</h3><p class="story-meta">${esc(x.contributor)}</p><p>${esc(x.story.slice(0, 140))}…</p><a href="voice.html"><strong>${tr("visit_voices")} →</strong></a></article>`
      )
      .join("");
  }
  const impact = qs("#impact-stats");
  if (impact) {
    const creators = publicProfiles().length;
    const published = read(DB.submissions).filter((x) => x.status === "Published").length;
    const works = read(DB.portfolio).length;
    const cats = new Set(publicProfiles().map((p) => p.area)).size;
    const groups = publicProfiles().filter((p) => p.kind === "troupe" || p.kind === "community_group" || p.kind === "organisation").length;
    const library = read(DB.library).filter((x) => x.visibility === "public" || x.status === "published").length;
    const projects = read(DB.projects).length;
    const accepted = read(DB.collabs).filter((c) => c.status === "Accepted").length;
    impact.innerHTML = `<div class="stat-grid">
      <div class="stat"><strong>${creators}</strong><span>${tr("stat_people")}</span></div>
      <div class="stat"><strong>${works}</strong><span>${tr("stat_works")}</span></div>
      <div class="stat"><strong>${published}</strong><span>${tr("stat_stories")}</span></div>
      <div class="stat"><strong>${cats}</strong><span>${tr("stat_areas")}</span></div>
      <div class="stat"><strong>${projects}</strong><span>${tr("stat_projects")}</span></div>
      <div class="stat"><strong>${accepted}</strong><span>${tr("stat_collabs")}</span></div>
      <div class="stat"><strong>${library}</strong><span>${tr("stat_library")}</span></div>
    </div>`;
  }
  const fg = qs("#featured-group");
  if (fg) {
    const troupe = publicProfiles().find((p) => p.id === "prof-intayoberana") || publicProfiles().find((p) => p.kind === "troupe");
    if (troupe) {
      fg.innerHTML = `<div class="section-head"><div><div class="eyebrow">${tr("featured_group")}</div><h2>${esc(troupe.displayName)}</h2></div><p>${esc(troupe.bio || "")}</p></div>
        <p class="story-meta">${tr("kind_troupe_one")} · ${esc(areaById(troupe.area).name)}</p>
        <div class="actions"><a class="btn blue" href="creator.html?id=${encodeURIComponent(troupe.id)}">${tr("view_profile")}</a>
        <a class="btn ghost" href="events.html">${tr("open_events")}</a></div>`;
    }
  }
  const ev = qs("#home-events");
  if (ev) renderEvents(ev);
}

function locKey(p) {
  if (p.locationKey) return p.locationKey;
  const t = (p.location || "").toLowerCase();
  if (t.includes("kigali")) return "kigali";
  if (t.includes("huye")) return "huye";
  if (t.includes("musanze")) return "musanze";
  if (t.includes("nyamata")) return "nyamata";
  if (t.includes("diaspora") || t.includes("mauritius") || p.area === "diaspora") return "diaspora";
  return "unlisted";
}

function renderEvents(box) {
  box = box || qs("#event-grid");
  if (!box) return;
  const events = read(DB.events);
  const profiles = read(DB.profiles);
  box.innerHTML =
    events
      .map((e) => {
        const host = profiles.find((p) => p.id === e.hostId);
        return `<article class="card">
      ${e.isDemo ? `<span class="tag demo-tag">${tr("illustrative_event")}</span>` : ""}
      <span class="tag">${esc(e.type || "")}</span><h3>${esc(e.title)}</h3>
      <p class="story-meta">${esc(e.date || "")}${e.location ? " · " + esc(e.location) : ""}</p>
      ${host ? `<p class="story-meta">${tr("hosted_by")} <a href="creator.html?id=${encodeURIComponent(host.id)}">${esc(host.displayName)}</a></p>` : ""}
      <p>${esc(e.description || "")}</p>
      ${host ? `<div class="actions"><a class="btn small" href="creator.html?id=${encodeURIComponent(host.id)}">${tr("view_profile")}</a></div>` : ""}
    </article>`;
      })
      .join("") || `<div class="empty">${tr("no_events")}</div>`;
}

function renderDiscover() {
  const box = qs("#discover-areas");
  if (!box) return;
  box.innerHTML = localizedAreas()
    .map(
      (a) => `<article class="card area-card" id="${a.id}">
      <div class="icon">${a.icon}</div>
      <h2>${esc(a.name)}</h2>
      <p><strong>${tr("lbl_meaning")}</strong> ${esc(a.meaning)}</p>
      <p><strong>${tr("lbl_people")}</strong> ${esc(a.people)}</p>
      <p><strong>${tr("lbl_preserve")}</strong> ${esc(a.preserve)}</p>
      <p><strong>${tr("lbl_upload")}</strong> ${esc(a.upload)}</p>
      <p><strong>${tr("lbl_participate")}</strong> ${esc(a.participate)}</p>
      <p><strong>${tr("lbl_connect")}</strong> ${esc(a.connect)}</p>
      <div class="actions">
        <a class="btn blue small" href="creators.html?area=${a.id}">${tr("meet_practitioners")}</a>
        <a class="btn ghost small" href="register.html">${tr("create_a_profile")}</a>
      </div>
    </article>`
    )
    .join("");
}

function renderCreators() {
  const box = qs("#creators-grid");
  if (!box) return;
  const areaSel = qs("#creator-area");
  if (areaSel && !areaSel.dataset.filled) {
    areaSel.innerHTML =
      `<option value="all">${tr("all_areas")}</option>` +
      localizedAreas()
        .map((a) => `<option value="${a.id}">${esc(a.name)}</option>`)
        .join("");
    areaSel.dataset.filled = "1";
  } else if (areaSel) {
    areaSel.options[0].textContent = tr("all_areas");
    localizedAreas().forEach((a, i) => {
      if (areaSel.options[i + 1]) areaSel.options[i + 1].textContent = a.name;
    });
  }
  const q = (qs("#creator-search")?.value || "").toLowerCase().trim();
  const area = qs("#creator-area")?.value || param("area") || "all";
  const kind = qs("#creator-kind")?.value || param("kind") || "all";
  const location = qs("#creator-location")?.value || param("location") || "all";
  if (qs("#creator-area") && param("area") && !qs("#creator-area").dataset.ready) {
    qs("#creator-area").value = param("area");
    qs("#creator-area").dataset.ready = "1";
  }
  if (qs("#creator-kind") && param("kind") && !qs("#creator-kind").dataset.ready) {
    qs("#creator-kind").value = param("kind");
    qs("#creator-kind").dataset.ready = "1";
  }
  if (qs("#creator-location") && param("location") && !qs("#creator-location").dataset.ready) {
    qs("#creator-location").value = param("location");
    qs("#creator-location").dataset.ready = "1";
  }
  const list = publicProfiles().filter((p) => {
    const blob = (p.displayName + (p.role || "") + (p.location || "") + (p.bio || "") + (p.skills || "") + (p.communityNote || "") + areaById(p.area).name).toLowerCase();
    const okQ = !q || blob.includes(q);
    const okA = area === "all" || p.area === area;
    const okK = kind === "all" || p.kind === kind;
    const okL = location === "all" || locKey(p) === location;
    return okQ && okA && okK && okL;
  });
    box.innerHTML = list.length ? list.map(creatorCard).join("") : `<div class="empty">${tr("no_creators")}</div>`;
}

function bindCreatorFilters() {
  ["creator-search", "creator-area", "creator-kind", "creator-location"].forEach((id) => {
    const el = qs("#" + id);
    if (!el) return;
    el.addEventListener("input", renderCreators);
    el.addEventListener("change", renderCreators);
  });
}

function renderCreator() {
  const id = param("id");
  const p = profileById(id);
  const root = qs("#creator-profile");
  if (!root) return;
  if (!p || !p.isPublic) {
    root.innerHTML = `<div class="empty">${tr("profile_private")}</div>`;
    return;
  }
  const area = areaById(p.area);
  const works = portfolioFor(p.id);
  const u = currentUser();
  const mine = u && myProfile(u.id) && myProfile(u.id).id === p.id;
  const followBtn = mine
    ? ""
    : `<button class="btn ghost" type="button" onclick="toggleFollow('${p.id}')">${isFollowing(p.id) ? tr("following") : tr("follow")}</button>`;
  const collabBtn = mine
    ? ""
    : `<button class="btn clay" type="button" onclick="openCollab('${p.id}')">${tr("request_collab")}</button>`;
  const websiteBtn = p.website
    ? `<a class="btn ghost" href="${esc(p.website)}" rel="noopener noreferrer" target="_blank">${tr("visit_website")}</a>`
    : "";
  const practices = practicesList(p);
  const available = p.available || [];
  root.innerHTML = `
    <div class="profile-hero">
      ${avatarHtml(p, "large")}
      <div>
        ${p.isDemo ? `<span class="tag demo-tag">${tr("demo_profile")}</span>` : ""}
        ${!p.isDemo && p.kind === "troupe" ? `<span class="tag">${tr("listed_org")}</span>` : ""}
        ${p.kind === "troupe" ? `<span class="tag">${tr("kind_org")}</span>` : p.kind === "community_group" ? `<span class="tag">${tr("kind_community")}</span>` : ""}
        ${p.curated ? `<span class="tag curated">${tr("curated")}</span>` : ""}
        <h1>${esc(p.displayName)}</h1>
        <p class="lead">${esc(p.kind === "troupe" ? tr("kind_org") : p.role || tr("practitioner"))} · ${esc(area.name)}</p>
        ${p.location ? `<p class="story-meta">${esc(p.location)}</p>` : ""}
        <p class="story-meta">${followerCount(p.id)} ${tr("followers")} · ${works.length} ${tr("works")}</p>
        <div class="actions">${followBtn}${collabBtn}${websiteBtn}<a class="btn ghost" href="creators.html">${tr("all_creators")}</a></div>
      </div>
    </div>
    <div class="grid two" style="margin-top:28px">
      <article class="card"><h3>${tr("biography")}</h3><p>${esc(p.bio || "—")}</p>
        ${p.background ? `<h3>${tr("cultural_context")}</h3><p>${esc(p.background)}</p>` : ""}
        ${p.communityNote ? `<h3>${tr("community")}</h3><p>${esc(p.communityNote)}</p>` : ""}</article>
      <article class="card">
        ${p.languages ? `<h3>${tr("languages")}</h3><p>${esc(p.languages)}</p>` : ""}
        ${practices.length ? `<h3>${tr("practices")}</h3><p>${practices.map((x) => `<span class="tag">${esc(x)}</span>`).join(" ")}</p>` : ""}
        ${available.length ? `<h3>${tr("available_for")}</h3><p>${available.map((x) => `<span class="tag">${esc(x)}</span>`).join(" ")}</p>` : ""}
        <p class="help">${tr("private_contact")}</p>
      </article>
    </div>
    <h2 style="margin-top:36px">${tr("portfolio")}</h2>
    <div class="grid">${
      works.length
        ? works
            .map(
              (w) => `<article class="card"><span class="tag">${esc(w.type)}</span><h3>${esc(w.title)}</h3>
          ${w.description ? `<p>${esc(w.description)}</p>` : ""}
          ${w.context ? `<p class="story-meta">${esc(w.context)}</p>` : ""}
          ${w.date || w.mediaName ? `<p class="story-meta">${w.date ? esc(w.date) : ""} ${w.mediaName ? "· " + esc(w.mediaName) : ""}</p>` : ""}
          ${w.link ? `<p><a href="${esc(w.link)}" rel="noopener noreferrer">${esc(w.link)}</a></p>` : ""}</article>`
            )
            .join("")
        : `<div class="empty">${tr("no_portfolio")}</div>`
    }</div>
    <div id="collab-box"></div>`;
  renderMeetArt(p, !!(u && !mine));
}

function openCollab(profileId) {
  const u = currentUser();
  if (!u) {
    location.href = "login.html";
    return;
  }
  const box = qs("#collab-box");
  if (!box) return;
  box.innerHTML = `<form class="form-card" onsubmit="sendCollab(event,'${profileId}')">
    <h3>${tr("request_collab")}</h3>
    <p class="help">${tr("collab_help")}</p>
    <label>${tr("collab_type")}</label>
    <select id="collab-type">${COLLAB_TYPES.map((t) => `<option>${esc(t)}</option>`).join("")}</select>
    <label>${tr("short_message")}</label>
    <textarea id="collab-msg" rows="5" required></textarea>
    <div class="actions"><button class="btn clay" type="submit">${tr("send_request")}</button></div>
    <div id="collab-result" class="help"></div>
  </form>`;
  box.scrollIntoView({ behavior: "smooth" });
}

function sendCollab(e, profileId) {
  e.preventDefault();
  const u = currentUser();
  if (!u) return;
  const a = read(DB.collabs);
  a.unshift({
    id: uid("col"),
    fromUserId: u.id,
    fromName: u.name,
    toProfileId: profileId,
    type: qs("#collab-type").value,
    message: qs("#collab-msg").value.trim(),
    status: "Pending",
    at: new Date().toISOString(),
  });
  write(DB.collabs, a);
  qs("#collab-result").innerHTML = '<span class="success-text">' + tr("collab_sent") + "</span>";
  e.target.reset();
}

function renderDashboard() {
  const u = requireAuth("contributor");
  if (!u) return;
  qs("#welcome").textContent = "Welcome, " + u.name;
  const stories = read(DB.submissions).filter((x) => x.userId === u.id);
  qs("#total").textContent = stories.length;
  qs("#pending").textContent = stories.filter((x) => x.status === "Pending").length;
  qs("#published").textContent = stories.filter((x) => x.status === "Published").length;
  const prof = myProfile(u.id);
  qs("#dash-profile-state").textContent = prof && prof.isPublic ? "Public cultural profile" : "Profile not public yet";
  const b = qs("#submission-list");
  b.innerHTML = stories.length
    ? stories
        .map(
          (x) =>
            `<tr><td><strong>${esc(x.title)}</strong></td><td>${esc(x.type)}</td><td>${statusBadge(x.status)}</td><td>${new Date(x.submittedAt).toLocaleDateString()}</td><td>${esc(x.feedback || "—")}</td></tr>`
        )
        .join("")
    : '<tr><td colspan="5"><div class="empty">No submissions yet. Share your first cultural story.</div></td></tr>';
  const inbox = qs("#collab-inbox");
  if (inbox && prof) {
    const mine = read(DB.collabs).filter((c) => c.toProfileId === prof.id);
    inbox.innerHTML = mine.length
      ? mine
          .map(
            (c) => `<tr>
        <td>${esc(c.fromName)}</td><td>${esc(c.type)}</td><td>${esc(c.message)}</td>
        <td>${statusBadge(c.status)}</td>
        <td>${
          c.status === "Pending"
            ? `<button class="btn success small" onclick="setCollab('${c.id}','Accepted')">Accept</button>
               <button class="btn danger small" onclick="setCollab('${c.id}','Declined')">Decline</button>`
            : esc(c.status)
        }</td></tr>`
          )
          .join("")
      : '<tr><td colspan="5"><div class="empty">No collaboration requests yet.</div></td></tr>';
  }
  const port = qs("#dash-portfolio");
  if (port && prof) {
    const items = portfolioFor(prof.id);
    port.innerHTML = items.length
      ? items.map((w) => `<tr><td>${esc(w.title)}</td><td>${esc(w.type)}</td><td>${esc(w.date || "—")}</td>
        <td><button class="btn danger small" onclick="deletePortfolio('${w.id}')">Remove</button></td></tr>`).join("")
      : '<tr><td colspan="4"><div class="empty">No portfolio items. Add one from My Cultural Profile.</div></td></tr>';
  }
  renderMeetArt(prof, true);
}

function setCollab(id, status) {
  const a = read(DB.collabs);
  const x = a.find((c) => c.id === id);
  if (!x) return;
  x.status = status;
  write(DB.collabs, a);
  renderDashboard();
}

function renderProfileForm() {
  const u = requireAuth("contributor");
  if (!u) return;
  let p = myProfile(u.id);
  if (!p) {
    p = {
      id: uid("prof"),
      userId: u.id,
      displayName: u.name,
      area: "oral",
      kind: "individual",
      role: "",
      location: "",
      languages: "",
      bio: "",
      background: "",
      skills: "",
      available: [],
      isPublic: false,
      curated: false,
      isDemo: false,
    };
    const all = read(DB.profiles);
    all.push(p);
    write(DB.profiles, all);
  }
  qs("#displayName").value = p.displayName || "";
  if (qs("#kind")) qs("#kind").value = p.kind || "individual";
  qs("#role").value = p.role || "";
  qs("#location").value = p.location || "";
  qs("#languages").value = p.languages || "";
  qs("#bio").value = p.bio || "";
  qs("#background").value = p.background || "";
  qs("#skills").value = p.skills || "";
  qs("#area").value = p.area || "oral";
  qs("#isPublic").checked = !!p.isPublic;
  const wrap = qs("#avail-wrap");
  wrap.innerHTML = AVAIL_OPTIONS.map(
    (o) => `<label class="check-pill"><input type="checkbox" value="${esc(o)}" ${(p.available || []).includes(o) ? "checked" : ""}> ${esc(o)}</label>`
  ).join("");
  qs("#type").innerHTML = PORTFOLIO_TYPES.map((t) => `<option>${esc(t)}</option>`).join("");
  renderDashPortfolioMini(p.id);
}

function renderDashPortfolioMini(profileId) {
  const box = qs("#portfolio-list");
  if (!box) return;
  const items = portfolioFor(profileId);
  box.innerHTML = items.length
    ? items
        .map(
          (w) => `<article class="card"><strong>${esc(w.title)}</strong><p class="story-meta">${esc(w.type)} · ${esc(w.mediaName || "no file")}</p>
      <button class="btn danger small" type="button" onclick="deletePortfolio('${w.id}')">Remove</button></article>`
        )
        .join("")
    : '<p class="help">No portfolio items yet.</p>';
}

function saveProfile(e) {
  e.preventDefault();
  const u = requireAuth("contributor");
  if (!u) return;
  const all = read(DB.profiles);
  const p = all.find((x) => x.userId === u.id);
  if (!p) return;
  p.displayName = qs("#displayName").value.trim();
  if (qs("#kind")) p.kind = qs("#kind").value;
  p.role = qs("#role").value.trim();
  p.location = qs("#location").value.trim();
  p.languages = qs("#languages").value.trim();
  p.bio = qs("#bio").value.trim();
  p.background = qs("#background").value.trim();
  p.skills = qs("#skills").value.trim();
  p.area = qs("#area").value;
  p.isPublic = qs("#isPublic").checked;
  p.available = [...document.querySelectorAll("#avail-wrap input:checked")].map((i) => i.value);
  write(DB.profiles, all);
  qs("#profile-result").innerHTML = '<span class="success-text">Profile saved. Public profiles appear in Creators.</span>';
}

function addPortfolio(e) {
  e.preventDefault();
  const u = requireAuth("contributor");
  if (!u) return;
  const p = myProfile(u.id);
  const f = qs("#p-media").files[0];
  const a = read(DB.portfolio);
  a.unshift({
    id: uid("port"),
    profileId: p.id,
    title: qs("#p-title").value.trim(),
    type: qs("#type").value,
    description: qs("#p-desc").value.trim(),
    context: qs("#p-context").value.trim(),
    link: qs("#p-link").value.trim(),
    date: qs("#p-date").value,
    mediaName: f ? f.name : "",
  });
  write(DB.portfolio, a);
  e.target.reset();
  qs("#port-result").innerHTML =
    '<span class="success-text">Item added. In this prototype only the file name is stored, not the file itself.</span>';
  renderDashPortfolioMini(p.id);
}

function deletePortfolio(id) {
  write(
    DB.portfolio,
    read(DB.portfolio).filter((x) => x.id !== id)
  );
  const u = currentUser();
  if (qs("#portfolio-list") && u) renderDashPortfolioMini(myProfile(u.id).id);
  if (qs("#dash-portfolio")) renderDashboard();
}

function renderVoices() {
  const a = read(DB.submissions).filter((x) => x.status === "Published");
  const box = qs("#community-stories");
  if (!box) return;
  const cat = qs("#voice-filter")?.value || "all";
  const list = a.filter((x) => cat === "all" || (x.category || x.type) === cat);
  box.innerHTML = list.length
    ? list
        .map(
          (x) => `<article class="card story-card"><div><span class="tag">${esc(x.category || x.type)}</span> ${x.demo ? '<span class="tag demo-tag">Demo story</span>' : ""}</div>
      <h3>${esc(x.title)}</h3>
      <div class="story-meta">${tr("shared_by")} ${esc(x.contributor)} · ${new Date(x.publishedAt || x.submittedAt).toLocaleDateString()}</div>
      <p class="story-text">${esc(x.story)}</p>
      <div class="story-meta">${esc(x.mediaName)} · ${tr("consent_provided")}</div></article>`
        )
        .join("")
    : `<div class="empty">${tr("no_stories")}</div>`;
}

function renderProjects() {
  const box = qs("#projects-grid"),
    sel = qs("#project-filter"),
    search = qs("#project-search");
  if (!box) return;
  const draw = () => {
    const cat = sel?.value || "all";
    const term = (search?.value || "").toLowerCase();
    const a = read(DB.projects).filter((p) => (cat === "all" || p.category === cat) && (p.title + p.description).toLowerCase().includes(term));
    box.innerHTML = a.length
      ? a
          .map(
            (p) =>
              `<article class="card"><div class="icon">${p.category === "archive" ? "◉" : p.category === "performance" ? "♪" : "✦"}</div><span class="tag">${esc(p.category)}</span><h3>${esc(p.title)}</h3><p>${esc(p.description)}</p></article>`
          )
          .join("")
      : `<div class="empty">${tr("no_projects")}</div>`;
  };
  sel && sel.addEventListener("change", draw);
  search && search.addEventListener("input", draw);
  draw();
}

function renderOpportunities() {
  const box = qs("#opp-grid");
  if (!box) return;
  const cat = qs("#opp-filter")?.value || "all";
  const list = read(DB.opportunities).filter((o) => cat === "all" || o.category === cat);
  box.innerHTML = list
    .map(
      (o) => `<article class="card"><span class="tag demo-tag">${tr("demo_listing")}</span>
      <span class="tag">${esc(o.category)}</span>
      <h3>${esc(o.title)}</h3>
      <p class="story-meta">${esc(o.location)}</p>
      <p>${esc(o.description)}</p>
      <p class="help">${tr("illustrative")}</p></article>`
    )
    .join("");
}

function sendContact(e) {
  e.preventDefault();
  const a = read(DB.contacts);
  a.unshift({
    id: uid("contact"),
    name: qs("#c-name").value.trim(),
    email: qs("#c-email").value.trim().toLowerCase(),
    role: qs("#c-role").value,
    message: qs("#c-message").value.trim(),
    createdAt: new Date().toISOString(),
  });
  write(DB.contacts, a);
  qs("#contact-result").innerHTML = '<span class="success-text">' + tr("contact_thanks") + "</span>";
  e.target.reset();
}

function renderAdmin() {
  const u = requireAuth("admin");
  if (!u) return;
  const a = read(DB.submissions);
  const profiles = read(DB.profiles);
  const collabs = read(DB.collabs);
  const works = read(DB.portfolio);
  const diaspora = profiles.filter((p) => p.area === "diaspora").length;
  qs("#a-total").textContent = a.length;
  qs("#a-pending").textContent = a.filter((x) => x.status === "Pending").length;
  qs("#a-published").textContent = a.filter((x) => x.status === "Published").length;
  qs("#a-contacts").textContent = read(DB.contacts).length;
  if (qs("#a-creators")) qs("#a-creators").textContent = profiles.filter((p) => !p.isDemo || p.isPublic).length;
  if (qs("#a-areas")) qs("#a-areas").textContent = new Set(profiles.filter((p) => p.isPublic).map((p) => p.area)).size;
  if (qs("#a-collabs")) qs("#a-collabs").textContent = collabs.length;
  if (qs("#a-works")) qs("#a-works").textContent = works.length;
  if (qs("#a-diaspora")) qs("#a-diaspora").textContent = diaspora;
  renderAdminStories();
  renderAdminContacts();
  renderAdminProjects();
  renderAdminCreators();
  renderAdminLibrary();
  renderAdminModeration();
}

function renderAdminLibrary() {
  const box = qs("#admin-library");
  if (!box) return;
  const items = read(DB.library);
  box.innerHTML = items.length
    ? items
        .map(
          (x) => `<tr><td>${esc(x.title)}</td><td>${esc(x.type)}</td><td>${esc(x.author || "")}</td>
      <td>${esc(x.visibility)}</td><td>${esc(x.status)}</td><td>${esc(x.fileName || "name only")}</td></tr>`
        )
        .join("")
    : '<tr><td colspan="6">No library items.</td></tr>';
}

function addLibraryItem(e) {
  e.preventDefault();
  const a = read(DB.library);
  a.unshift({
    id: uid("lib"),
    title: qs("#lib-title").value.trim(),
    type: qs("#lib-type").value,
    area: qs("#lib-area").value,
    author: qs("#lib-author").value.trim(),
    visibility: qs("#lib-vis").value,
    status: "published",
    fileName: qs("#lib-file").files[0] ? qs("#lib-file").files[0].name : "",
    description: qs("#lib-desc").value.trim(),
  });
  write(DB.library, a);
  const act = read(DB.activity);
  act.unshift({ action: "Publication added", item: qs("#lib-title").value.trim(), at: new Date().toISOString() });
  write(DB.activity, act);
  e.target.reset();
  renderAdminLibrary();
}

function renderAdminModeration() {
  const box = qs("#admin-reports");
  if (!box) return;
  const items = read(DB.reports);
  box.innerHTML = items.length
    ? items
        .map(
          (x) => `<tr><td>${esc(x.itemType || x.type || "")} ${esc(x.itemId || x.id || "")}</td>
      <td>${esc(x.reason)}</td><td>${esc(x.status || "new")}</td>
      <td><div class="row-actions cols-2"><button class="btn small" type="button" onclick="moderationDecide('${x.id}','restore')">Restore</button>
      <button class="btn ghost small" type="button" onclick="moderationDecide('${x.id}','suspend')">Suspend</button></div></td></tr>`
        )
        .join("")
    : '<tr><td colspan="4">No reports. Inspect first — reports never auto-delete.</td></tr>';
}

function moderationDecide(id, decision) {
  const a = read(DB.reports);
  const x = a.find((r) => r.id === id);
  if (!x) return;
  x.status = decision === "restore" ? "resolved" : "under_review";
  write(DB.reports, a);
  if (x.itemType === "profile" || x.type === "profile") {
    const profiles = read(DB.profiles);
    const p = profiles.find((pr) => pr.id === x.itemId);
    if (p) {
      p.moderationStatus = decision === "restore" ? "active" : "suspended";
      write(DB.profiles, profiles);
    }
  }
  renderAdminModeration();
}

function renderAdminStories() {
  const a = read(DB.submissions),
    b = qs("#admin-list");
  if (!b) return;
  b.innerHTML = a.length
    ? a
        .map(
          (x) => `<tr><td><strong>${esc(x.title)}</strong><br><span class="story-meta">${esc(x.mediaName)}</span></td>
      <td>${esc(x.contributor)}</td><td>${x.consent ? "✓ Provided" : "No"}</td>
      <td>${statusBadge(x.status)}</td>
      <td class="hide-mobile">${esc(x.story.slice(0, 90))}${x.story.length > 90 ? "…" : ""}</td>
      <td>${adminActions(x)}</td></tr>`
        )
        .join("")
    : '<tr><td colspan="6"><div class="empty">No submissions.</div></td></tr>';
}
function adminActions(x) {
  if (x.status === "Pending")
    return `<div class="row-actions cols-2"><button class="btn success small" onclick="reviewStory('${x.id}','Approved')">Approve</button><button class="btn danger small" onclick="reviewStory('${x.id}','Rejected')">Reject</button></div>`;
  if (x.status === "Approved") return `<div class="row-actions cols-2"><button class="btn small" onclick="publishStory('${x.id}')">Publish</button></div>`;
  if (x.status === "Rejected") return `<div class="row-actions cols-2"><button class="btn ghost small" onclick="reviewStory('${x.id}','Pending')">Reopen</button></div>`;
  return "Published";
}
function reviewStory(id, status) {
  const a = read(DB.submissions),
    x = a.find((s) => s.id === id);
  if (!x) return;
  if (status === "Rejected") x.feedback = prompt("Reason for rejection:", "Please review the consent or cultural context.") || "Rejected after review.";
  else if (status === "Approved") x.feedback = "Approved after consent and cultural-sensitivity review.";
  else x.feedback = "";
  x.status = status;
  write(DB.submissions, a);
  renderAdmin();
}
function publishStory(id) {
  const a = read(DB.submissions),
    x = a.find((s) => s.id === id);
  if (!x || x.status !== "Approved") return;
  if (!x.consent) {
    alert("Consent must be provided before publishing.");
    return;
  }
  x.status = "Published";
  x.publishedAt = new Date().toISOString();
  write(DB.submissions, a);
  renderAdmin();
}
function renderAdminContacts() {
  const b = qs("#contact-list"),
    a = read(DB.contacts);
  if (!b) return;
  b.innerHTML = a.length
    ? a
        .map(
          (x) =>
            `<tr><td>${esc(x.name)}</td><td>${esc(x.role)}</td><td>${esc(x.email)}</td><td>${esc(x.message)}</td><td>${new Date(x.createdAt).toLocaleDateString()}</td></tr>`
        )
        .join("")
    : '<tr><td colspan="5"><div class="empty">No contact messages yet.</div></td></tr>';
}
function renderAdminProjects() {
  const b = qs("#admin-projects"),
    a = read(DB.projects);
  if (!b) return;
  b.innerHTML = a
    .map(
      (x) =>
        `<tr><td>${esc(x.title)}</td><td>${esc(x.category)}</td><td>${esc(x.description)}</td><td><button class="btn danger small" onclick="deleteProject('${x.id}')">Delete</button></td></tr>`
    )
    .join("");
}
function addProject(e) {
  e.preventDefault();
  const a = read(DB.projects);
  a.push({
    id: uid("project"),
    title: qs("#p-title").value.trim(),
    category: qs("#p-category").value,
    description: qs("#p-description").value.trim(),
  });
  write(DB.projects, a);
  e.target.reset();
  renderAdminProjects();
}
function deleteProject(id) {
  if (!confirm("Delete this project?")) return;
  write(
    DB.projects,
    read(DB.projects).filter((x) => x.id !== id)
  );
  renderAdminProjects();
}
function renderAdminCreators() {
  const b = qs("#admin-creators");
  if (!b) return;
  b.innerHTML = read(DB.profiles)
    .map(
      (p) => `<tr>
      <td>${esc(p.displayName)} ${p.isDemo ? "(demo)" : ""}</td>
      <td>${esc(areaById(p.area).name)}</td>
      <td>${esc(p.location || "—")}</td>
      <td>${p.isPublic ? "Public" : "Private"}</td>
      <td>${p.curated ? "Yes" : "No"}</td>
      <td><div class="row-actions cols-2"><button class="btn small" onclick="toggleCurated('${p.id}')">${p.curated ? "Uncurate" : "Curate"}</button></div></td>
    </tr>`
    )
    .join("");
}
function toggleCurated(id) {
  const a = read(DB.profiles);
  const p = a.find((x) => x.id === id);
  if (!p) return;
  p.curated = !p.curated;
  write(DB.profiles, a);
  renderAdmin();
}
function showAdminTab(id, btn) {
  document.querySelectorAll(".admin-panel").forEach((x) => x.classList.remove("active"));
  document.querySelectorAll(".tab").forEach((x) => x.classList.remove("active"));
  qs("#" + id).classList.add("active");
  btn.classList.add("active");
}
