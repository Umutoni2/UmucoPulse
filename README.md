# UmucoPulse

A Rwandan cultural heritage platform for documenting stories, showcasing cultural practitioners, and building a community archive.

* **Live Demo (Render):** [https://umucopulse.onrender.com/]
* **Source Code:** https://github.com/umutoni2/UmucoPulse
* **SRS:** https://drive.google.com/file/d/1oDTsxYcGhEV7IFH40yBdwD-M7Fi-1KFc/view?usp=drive_link
---

## What this project contains

UmucoPulse is a web platform designed to help preserve and share Rwandan cultural heritage through digital storytelling and community participation.

The project has three main parts:

| **Location**      | **What it is**                                                                                                              |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `app/` + `run.py` | **Main Flask application** with authentication, database, contributor profiles, story submissions, and administrator review |
| `docs/`           | **GitHub Pages prototype** of the platform and its main user flows                                                          |
| `legacy/`         | Original static version of the project                                                                                      |

The **Flask application is the main version of the project and is deployed on Render**. The GitHub Pages version is kept as a prototype and alternative way of viewing the interface.

---

## Actors

### Visitor

Visitors can:

* View the home page
* Discover cultural content
* View creators and their work
* Read published stories and voices
* View projects and opportunities
* Learn more about UmucoPulse
* Send messages through the contact page

### Contributor

Contributors can:

* Create an account
* Create and update their cultural profile
* Make their profile public
* Add portfolio information
* Submit cultural stories
* Give consent when submitting stories
* Follow creators
* Send collaboration requests

### Administrator

Administrators can:

* Review submitted stories
* Approve or reject submissions
* Provide feedback on rejected submissions
* Publish approved stories
* Manage projects
* Manage messages
* Manage curated creator profiles
* View simple platform statistics

---

## Main Processes Demonstrated

The main user flows in the application include:

1. Browse the different cultural sections of the platform
2. Register as a contributor
3. Create a cultural profile
4. Add portfolio information
5. Submit a cultural story with consent
6. Log in as an administrator
7. Review a submitted story
8. Approve or reject the story
9. Publish an approved story
10. View the published story under Voices
11. Follow a creator
12. Send a collaboration request
13. Accept or decline a collaboration request

The homepage also includes English, Kinyarwanda and French language labels.

---

## Demo Accounts

The following accounts can be used to test the application:

| **Role**      | **Email**               | **Password** |
| ------------- | ----------------------- | ------------ |
| Administrator | `admin@umucopulse.org`  | `Umuco123!`  |
| Contributor   | `sylvie@umucopulse.org` | `Story123!`  |

These accounts are provided for demonstration purposes.

The application is a student/class project, so the authentication and other security features should not be considered production-ready.

**Please change the passwords before using the system for real-world purposes.**

---

# A. Use the Live Render Application

The easiest way to test UmucoPulse is through the live Render deployment:

**Live Demo:** [https://umucopulse.onrender.com/]

You can open the link directly in a browser without installing Python or cloning the repository.

### Suggested Demo Flow

1. Open the home page
2. Explore Discover, Creators, Voices, Projects and Opportunities
3. Log in as a contributor
4. Open the cultural profile
5. Make the profile public
6. Add a portfolio note
7. Submit a cultural story
8. Include the required consent
9. Log out
10. Log in as the administrator
11. Open Story Submissions
12. Review the submitted story
13. Approve and publish it
14. Open Voices and confirm that the story is visible
15. Follow a creator
16. Send a collaboration request
17. Check the request status

---

# B. Run the Flask Application Locally

If you want to run the project locally, you need **Python 3.10 or newer**.

### 1. Clone the repository

```bash
git clone https://github.com/umutoni2/UmucoPulse.git
cd UmucoPulse
```

### 2. Create a virtual environment

**Windows PowerShell:**

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python run.py
```

### 5. Open the application

Go to:

**http://127.0.0.1:5000**

The UmucoPulse home page should appear.

### 6. Stop the application

Press:

```text
Ctrl + C
```

---

# C. GitHub Pages Prototype

The project also contains a static prototype inside the `docs/` folder.

It can be used to view the interface without running the Flask application.

To run it locally:

```bash
cd docs
python -m http.server 8000
```

Then open:

**http://localhost:8000**

The GitHub Pages version uses browser `localStorage` for its demo data. It is mainly intended as a prototype and does not replace the main Flask application.

---

## Project Structure

```text
UmucoPulse/
├── app/                  Flask application
│   ├── models.py
│   ├── forms.py
│   ├── routes/
│   │   ├── public.py
│   │   ├── auth.py
│   │   └── admin.py
│   ├── templates/
│   └── static/
├── docs/                 GitHub Pages prototype
├── legacy/               Original static version
├── config.py
├── run.py
├── requirements.txt
├── SRS.md
└── README.md
```

---

## Notes

* The Render deployment is the main public version of UmucoPulse.
* The GitHub Pages version is a static prototype.
* Demo data and creator profiles are for demonstration purposes.
* Media controls store file names rather than uploading actual media files.
* Authentication is implemented for the project demonstration and is not intended to be used as production-level security.
* The project does not claim government endorsement or real institutional partnerships.

---

## Author

**Sylvie Umutoni Rutaganira**

BSc Software Engineering
African Leadership College of Higher Education

**Module:** Introduction to Software Engineering

**GitHub:** https://github.com/umutoni2

**Project:** UmucoPulse — Rwandan Cultural Heritage Platform
