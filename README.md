# BLUS — Beijing Union of Liberian Students

A Django web platform for the Beijing Union of Liberian Students. It has a
public-facing marketing website and a private, role-aware dashboard area for
administrators and student members.

---

## ✨ Features

- **Public website** — Home, About, Leadership, Blog/News, Contact (animated with AOS + custom CSS).
- **Custom authentication** — email-based login (no usernames) with a custom `User` model and roles (`admin` / `student`).
- **Portal chooser** — visitors pick "Administrator" or "Student"; routing is decided by the user's real role, not the chosen door.
- **Two dashboards, one design** — admins and students share the same dashboard shell but see role-appropriate content and navigation.
- **Production-ready** — environment-driven settings, WhiteNoise static serving, and auto-switching SQLite ↔ Railway PostgreSQL.

---

## 🧱 Tech Stack

| Layer | Tech |
|---|---|
| Framework | Django 6.0.5 |
| Database | SQLite (local) · PostgreSQL (production, via Railway) |
| Styling | Tailwind (CDN) + `static/css/main.css` |
| Static files | WhiteNoise |
| Config | django-environ + dj-database-url |
| Server | Gunicorn |
| Hosting | Railway |

---

## 📁 Project Structure

```
Blus_web_app/
├── config/                  # Project settings, root URLs, WSGI/ASGI
│   ├── settings.py
│   └── urls.py
├── apps/
│   ├── accounts/            # Custom User model, auth (login/register/portal)
│   ├── administration/      # Admin dashboard logic + routing
│   ├── students/            # StudentProfile + student dashboard
│   ├── events/              # Event management
│   ├── finance/             # Finance records, dues, loans
│   └── blog/                # Posts / news
├── frontend/templates/frontend/   # Public pages + admin_dashboard.html
├── templates/
│   ├── base.html            # Public site shell
│   ├── base_admin.html      # Dashboard shell (admin sidebar)
│   └── base_student.html    # Dashboard shell (student sidebar)
├── static/css/main.css      # Shared component styles & animations
├── manage.py
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Dev dependencies
├── Procfile / railway.json  # Deployment config
└── .env.example             # Environment variable reference
```

---

## 🔐 Authentication & Roles

- Login is by **email + password** (`USERNAME_FIELD = "email"`).
- A user's `role` is either `admin` or `student`.
- **First admin:** `python manage.py createsuperuser` (sets role = admin).
- **More admins:** promote an existing user in the Django admin (`/admin/`) — set Role = Admin and tick `is_staff`.
- **Self-registration** always creates a **student** — nobody can self-promote to admin.

### Routing after login
| Role | Lands on |
|---|---|
| Admin / staff | `/dashboard/` → `administration:dashboard` |
| Student | `/students/student-dashboard/` → `students:student_dashboard` |

---

## 🗺️ Key URLs

| Path | Name | Purpose |
|---|---|---|
| `/` | `home` | Public home |
| `/about/` `/leadership/` `/news/` `/contact/` | — | Public pages |
| `/accounts/` | `accounts:portal` | Admin/Student chooser |
| `/accounts/login/` | `accounts:login` | Login (use `?as=admin` / `?as=student`) |
| `/accounts/register/` | `accounts:register` | Student sign-up |
| `/dashboard/` | `administration:dashboard` | Admin dashboard |
| `/students/student-dashboard/` | `students:student_dashboard` | Student dashboard |
| `/admin/` | — | Django admin site |

---

## 🚀 Local Setup

```bash
# 1. Clone and enter the project
cd Blus_web_app

# 2. Create & activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements-dev.txt

# 4. Create your .env (copy the example, then edit)
copy .env.example .env       # Windows
# cp .env.example .env        # macOS/Linux

# 5. Apply migrations
python manage.py migrate

# 6. Create your first admin
python manage.py createsuperuser

# 7. Run the dev server
python manage.py runserver
```

Visit http://127.0.0.1:8000.

> Locally, leave `DATABASE_URL` unset in `.env` → the app uses **SQLite** automatically.

---

## ⚙️ Environment Variables

See `.env.example` for the full list. The essentials:

| Variable | Local | Production (Railway) |
|---|---|---|
| `IS_PRODUCTION` | `False` | `True` |
| `DEBUG` | `True` | `False` |
| `SECRET_KEY` | any dev key | a strong, unique key |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost` | your Railway/custom domain |
| `CSRF_TRUSTED_ORIGINS` | `http://localhost:8000,...` | `https://your-domain` |
| `DATABASE_URL` | *(unset → SQLite)* | injected by Railway PostgreSQL plugin |

Generate a secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## ☁️ Deployment (Railway)

1. Push the repo to GitHub and connect it in Railway.
2. Add a **PostgreSQL** plugin — Railway injects `DATABASE_URL` automatically (do **not** set it by hand; reference it as `${{Postgres.DATABASE_URL}}` if needed).
3. Set these variables in the Railway dashboard:
   ```
   IS_PRODUCTION=True
   DEBUG=False
   SECRET_KEY=<your-key>
   ALLOWED_HOSTS=<your-app>.up.railway.app
   CSRF_TRUSTED_ORIGINS=https://<your-app>.up.railway.app
   ```
4. Deploy. `railway.json` runs migrations + `collectstatic` in `preDeployCommand`, then starts Gunicorn — so the healthcheck isn't blocked by startup work.

Run one-off commands against the live database:
```bash
railway run python manage.py createsuperuser
```

---

## 🎨 Styling Notes

- Shared component styles and animations live in **`static/css/main.css`** (single source of truth).
- Tailwind utilities load via CDN; the brand palette (`brand-blue #1A2B6B`, `brand-red #E02B20`) and fonts (Syne / DM Sans) are configured in the base templates.
- Page-specific styles use the `{% block extra_css %}` slot.

> **Static storage:** hashed/manifest storage (WhiteNoise) is used **only in production**. In development, plain storage serves files live — no `collectstatic` needed after each edit.

---

## 📌 Status

The frontend and auth/dashboard scaffolding are complete. Backend models for
events, finance, and blog are intentionally minimal and will be built out in
upcoming tasks.
