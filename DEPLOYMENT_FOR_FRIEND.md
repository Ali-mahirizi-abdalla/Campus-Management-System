# 🚀 Deployment Guide: Student Welfare Management System (SWMS)

This guide provides instructions for deploying the SWMS project to a production environment.

## 🛠️ Prerequisites
- Python 3.13+
- PostgreSQL or MySQL Database
- Redis (for Celery/Caching)
- A private GitHub repository for the code

---

## 📋 Step 1: Environment Configuration
1.  **Clone the Repository**:
    ```bash
    git clone <your-repo-url>
    cd Student-Welfare-Management-System
    ```
2.  **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    .\venv\Scripts\activate   # Windows
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set Up Environment Variables**:
    - Copy `.env.example` to `.env`.
    - Fill in the required secrets (SECRET_KEY, DB credentials, API keys).
    - **Crucial**: Set `DEBUG=False` and `USE_SQLITE=False` in production.

---

## 🗄️ Step 2: Database Setup (PostgreSQL Recommended)
1.  **Create Database**: Create a new database in PostgreSQL.
2.  **Configure URL**: Provide the `DATABASE_URL` in your `.env` file:
    `DATABASE_URL=postgres://user:password@host:port/dbname`
3.  **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

---

## 🎨 Step 3: Static & Media Files
1.  **Collect Static Files**:
    ```bash
    python manage.py collectstatic --noinput
    ```
2.  **Media Files**:
    - If using Cloudinary (recommended), set `USE_CLOUDINARY=True` and provide the keys in `.env`.
    - If using local storage, ensure the `media/` directory has write permissions.

---

## ⚡ Step 4: Background Tasks (Celery + Redis)
1.  **Redis**: Ensure Redis is running and the `REDIS_URL` is set in `.env`.
2.  **Run Celery Worker**:
    ```bash
    celery -A swms worker --loglevel=info
    ```
3.  **Run Celery Beat** (if needed for scheduled tasks):
    ```bash
    celery -A swms beat --loglevel=info
    ```

---

## 🚀 Step 5: Launching the Server
Use Gunicorn for the web server:
```bash
gunicorn swms.wsgi:application --bind 0.0.0.0:8000
```

### Nginx Configuration Template
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/your/project/static/;
    }

    location /media/ {
        alias /path/to/your/project/media/;
    }
}
```

---

## 🛡️ Security Checklist
- [ ] `DEBUG` is set to `False`.
- [ ] `SECRET_KEY` is a unique, long random string.
- [ ] `ALLOWED_HOSTS` contains only your production domain.
- [ ] `.env` is NOT committed to Git.
- [ ] SSL/TLS is configured (e.g., via Let's Encrypt).
- [ ] Database is password-protected and not publicly accessible.
