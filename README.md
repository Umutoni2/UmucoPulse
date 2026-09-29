# UmucoPulse

A Rwandan cultural heritage platform for documenting stories, showcasing practitioners, and growing a community archive.

- **Public demo (GitHub Pages):** https://umutoni2.github.io/UmucoPulse/
- **Source code:** https://github.com/umutoni2/UmucoPulse
- **SRS:** [SRS.md](./SRS.md)

If the Pages site still shows the old static homepage after you push, open the repository **Settings → Pages**, set **Source** to **Deploy from a branch**, branch **master** (or **main**), folder **/docs**, then Save. The public URL stays:

`https://umutoni2.github.io/UmucoPulse/`

---

## What this project contains

| Location | What it is |
|----------|------------|
| `app/` + `run.py` | **Version 2 — Flask app** with database, signup/login, contributor dashboard, admin review workflow |
| `docs/` | **Public GitHub Pages prototype** (HTML/CSS/JS). Same actors and screens, stored in the browser so graders can use a public URL without installing Python |
| `legacy/` | Original class portfolio site (first static version) |

### Actors (system design)

- **Visitor** — Home, Discover, Creators, Voices, Projects, Opportunities, About, Contact
- **Contributor** — register, profile, portfolio, stories with consent, follow, collaboration requests
- **Administrator** — review consent, approve/reject/publish, projects, messages, curated profiles, simple statistics

### Processes demonstrated

1. Browse cultural areas, creators, voices, projects and demo opportunities
2. Register → build a cultural profile → add a portfolio note → submit a story with consent
3. Admin: Pending → Approve or Reject (with feedback) → Publish to Voices
4. Follow a creator and send a collaboration request (Pending / Accepted / Declined)
5. EN / RW / FR labels on the homepage (not a full translation of every page)

---

## Demo accounts

Use these on both the Flask app and the GitHub Pages prototype:

| Role | Email | Password |
|------|--------|----------|
| Administrator | `admin@umucopulse.org` | `Umuco123!` |
| Contributor | `sylvie@umucopulse.org` | `Story123!` |

On GitHub Pages the contributor account is created when you register. The administrator account is created the first time the Pages site loads.

**Prototype limits:** Pages data is only in the current browser (`localStorage`). Media controls store file names, not files. Authentication is a class demo, not production security. Seeded creator profiles and opportunity listings are fictional and labelled as demo content. UmucoPulse does not claim government endorsement or real institutional partners.

Change these passwords before any real-world use.

---

## A. Run the Flask application (recommended for the video demo)

You need **Python 3.10 or newer**. On Windows, `python` should open from PowerShell or Command Prompt.

### 1. Open the project folder

```bash
cd C:\Users\USER\UmucoPulse
```

If you cloned from GitHub:

```bash
git clone https://github.com/umutoni2/UmucoPulse.git
cd UmucoPulse
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks the script, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of the line.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. (Optional) environment file

Copy `.env.example` to `.env` only if you want custom secrets. Defaults already work for local demo:

- Admin: `admin@umucopulse.org` / `Umuco123!`

### 5. Start the server

```bash
python run.py
```

### 6. Open the site

In a browser go to:

**http://127.0.0.1:5000**

You should see the UmucoPulse home page.

### 7. Stop the server

In the terminal press `Ctrl + C`.

### Flask pages to click during the demo

1. Home, Discover, Creators, Voices, Projects, Opportunities, About, Contact
2. Sign up → My cultural profile (make public) → Submit a story (tick consent)
3. Log out → Log in as administrator → Story Submissions → Approve → Publish
4. Open Voices and confirm the community story is listed
5. Follow a demo creator and send a collaboration request
6. Newsletter in the footer; EN / RW / FR in the header (homepage labels)

---

## B. Run the public Pages prototype locally (no Flask)

This uses the files in `docs/` (same flow as the live GitHub Pages URL).

```bash
cd docs
python -m http.server 8000
```

Open **http://localhost:8000**

Do not open the HTML file by double-clicking if login/register misbehaves; use this local server.

---

## C. Deploy Flask on Render (optional extra public URL)

1. Push this repository to GitHub (public).
2. Go to [https://render.com](https://render.com) and sign in with GitHub.
3. **New → Web Service →** select `umutoni2/UmucoPulse`.
4. Runtime: **Python**. Build: `pip install -r requirements.txt`. Start: `gunicorn run:app`.
5. Add environment variables `SECRET_KEY`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`.
6. Deploy. Copy the `onrender.com` URL into your Google Doc as a second live link.

The SQLite database on the free Render plan resets when the service sleeps; that is acceptable for a class demo. GitHub Pages remains the stable public URL.

---

## Project structure

```
UmucoPulse/
├── app/                  Flask application
│   ├── models.py
│   ├── forms.py
│   ├── routes/           public, auth, admin
│   ├── templates/
│   └── static/
├── docs/                 GitHub Pages public prototype
├── legacy/               original static portfolio
├── config.py
├── run.py
├── requirements.txt
├── SRS.md
└── README.md             this file
```

## Author

Sylvie Umutoni Rutaganira  
Introduction to Software Engineering  
GitHub: [umutoni2](https://github.com/umutoni2)
