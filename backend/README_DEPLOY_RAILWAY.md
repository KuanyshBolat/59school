Deployment to Railway (quick guide)

1) Create Railway project and connect your Git repository (select backend folder as project root).
2) Add Railway plugin: Managed Postgres. Copy the generated DATABASE_URL.
3) In Railway project settings -> Variables, set the following environment variables:
   - SECRET_KEY: a strong secret
   - DEBUG: False
   - ALLOWED_HOSTS: your-railway-app.up.railway.app,your-domain.com
   - DATABASE_URL: (from Railway Postgres)
   - CORS_ALLOWED_ORIGINS: https://your-frontend.vercel.app
   - CSRF_TRUSTED_ORIGINS: https://your-frontend.vercel.app
   - SECURE_SSL_REDIRECT: True
   - NEXT_PUBLIC_API_URL: https://your-railway-app.up.railway.app
4) Railway will detect a Python app (Procfile present). Build command: automatic. Start command from Procfile: gunicorn config.wsgi:application
5) After deploy completes, go to the deployed URL and run migrations from Railway console or via `python manage.py migrate`.

Migrate data from SQLite (optional):
- Locally: dump data `python manage.py dumpdata > dump.json`
- After setting DATABASE_URL to Postgres locally, run `python manage.py migrate` and then `python manage.py loaddata dump.json`.

Notes:
- For serving static files, we use WhiteNoise and collectstatic during build. Ensure `python manage.py collectstatic --noinput` is run during build (Railway runs collectstatic automatically if detected; otherwise add as build step).
- For media files, configure S3 or other storage if you need persistent upload storage.

