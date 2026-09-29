# UmucoPulse — Software Requirements Specification (extract for submission)

**Product:** UmocoPulse digital platform (Flask + public GitHub Pages prototype)  
**Author:** Sylvie Umutoni Rutaganira  
**Version:** 1.1 — 18 September 2026  

Full academic SRS (proposal, NFRs, references) lives with the formative document. This file maps the **implemented prototype** to SRS functional requirements so graders can trace screens.

## 1. Purpose

UmucoPulse is a cultural storytelling and archiving website for preserving and promoting Rwandan heritage. It starts as a founder-led platform and grows into a community archive with review before publication.

## 2. Problem (summary)

Rwandan oral culture is poorly digitized. Youth and diaspora mainly meet institutional or tourism sites, not a place to contribute their own stories. UmucoPulse provides a community archive with consent and cultural-sensitivity review.

## 3. Actors

| Actor | Prototype behaviour |
|--------|---------------------|
| Visitor / general public | Home, About, Skills, Projects, Mission, Voices, Contact, newsletter |
| Cultural practitioner / contributor | Sign up, log in, submit story with consent, dashboard statuses |
| Educator / student / diaspora | Same public pages; may register to contribute |
| Administrator (founder) | Login, review queue, approve, reject, publish, contacts, metrics, mentorship |

## 4. Functional requirements vs prototype

| ID | Requirement | Where it is |
|----|-------------|-------------|
| FR 1 / 1.1 / 1.2 | Homepage, hero, persistent nav | Home |
| FR 2 / 2.1 / 2.2 | About + quick facts | Home #about |
| FR 3 / 3.1 / 3.2 | Technical and cultural skills | Home #skills |
| FR 4 / 4.1 | Project cards | Home + Projects |
| FR 4.2 | Filter/search projects | Projects page |
| FR 5 / 5.1 / 5.2 | Mission, vision, focus areas | Mission |
| FR 5.3 | Focus-area progress | Mission metrics (Flask admin can edit) |
| FR 6.1 | Featured Voices | Voices |
| FR 6.2 | Community story submission | Register → Submit story |
| FR 6.3 | Consent + admin review | Tick consent; Admin Approve then Publish |
| FR 7.1 / 7.2 | Contact form + newsletter | Contact + footer |
| FR 7.3 | Acknowledgement | Flash / success message after submit |
| FR 8.1 | Language toggle | EN / RW / FR |
| FR 8.2 | Semantic markup, alt text | Templates |

## 5. Operation (login, signup, redirects)

- Signup creates a **contributor** and redirects to the contributor dashboard.
- Login sends **admin** to `/admin` and **contributor** to `/dashboard`.
- Submit story requires login; guests are redirected to login.
- Approve does not publish until the administrator clicks **Publish**.

## 6. Out of scope for this prototype

- Real email delivery of confirmations
- Full media file hosting on GitHub Pages (filename recorded in the static prototype)
- Production-grade multilingual translations of every paragraph
