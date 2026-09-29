# Video script (5–10 minutes)

Speak slowly and clearly. Record the browser at 1280×720 or larger. Do not rush the demo.

**Suggested title slide (10 seconds):**  
UmucoPulse — Sylvie Umutoni Rutaganira — Introduction to Software Engineering — Final prototype demo.

---

## 0:00–1:30  Description of the system

“UmucoPulse is a Rwandan cultural heritage organisation starting small with a digital platform. The software is a web application that documents traditions, shares cultural stories, and will grow into a community archive.

I built it in Agile increments: first a static portfolio, then an interactive prototype, then a Flask backend with a database.

Public pages are Home, Discover, Projects, Voices, About, and Contact. Registered contributors submit stories. The administrator reviews consent and cultural sensitivity before anything is published.”

Show the live URL in the address bar: `https://umutoni2.github.io/UmucoPulse/`  
Then say: “This public URL is the deployed prototype. I will also show the Flask version running locally so you can see signup, login, and the review workflow with a real database.”

---

## 1:30–3:00  Problem, why it is a problem, proposed solution

**Problem:** Much of Rwanda’s dance, poetry, music, and oral history lives in memory or on phones, not in an organised public archive. Young people and the diaspora spend time online but mostly see tourism sites, not a place to contribute.

**Why it is a problem:** When stories are not documented, they are harder to pass to the next generation. Practitioners have no shared digital home. Existing sites are static and institutional.

**Solution:** UmucoPulse. Visitors learn and browse. Contributors register, submit a story, and give consent. The founder-administrator reviews, approves, and publishes to Voices. That matches the SRS: FR 1 to FR 8, plus the actors Visitor, Contributor, and Administrator.

---

## 3:00–8:30  Demo (SRS + actors + processes)

Stay on one browser. Click; do not only scroll.

1. **Visitor — Home:** community hero (“Culture lives when people share it”), Discover / Contribute / Connect, four-step contribution path.  
2. **Discover:** oral history, music, dance, poetry, craft, diaspora themes.  
3. **Projects:** change the category filter and search.  
4. **About:** why the platform exists; founder is a note, not the whole site.  
5. **Voices:** published community archive.  
6. **Contact:** submit name, email, role, message — show the success message. Newsletter in the footer.  
7. **Language:** switch EN / RW / FR, show homepage headline change.  
8. **Signup:** create a new contributor (or use sylvie@umucopulse.org / Story123!). Show redirect to dashboard.  
9. **Submit story:** title, category, text longer than a sentence, tick consent, submit. Status **Pending**.  
10. **Logout → Admin login:** `admin@umucopulse.org` / `Umuco123!`  
11. **Admin:** pending story → **Approve** → **Publish**.  
12. **Voices** again: community story is visible.

Say out loud: “The contributor cannot publish themselves. That is the consent and sensitivity workflow from the SRS.”

---

## 8:30–9:30  Close

“The GitHub repository is public. The README lists every setup step: clone, virtual environment, pip install, python run.py. The SRS is linked from the repo. The product is publicly reachable on GitHub Pages.

Thank you.”

---

## Recording tips

- Test audio first; sit close to the microphone.  
- Disable extra notifications.  
- If GitHub Pages still shows the old site, demo `docs/` via `python -m http.server 8000` **and** Flask at `http://127.0.0.1:5000`, and still show the public URL in the address bar once Pages is updated.  
- Keep the clip between 5 and 10 minutes. Cut silences; do not speed through the workflow.
