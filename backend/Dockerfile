FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps for psycopg2 and building Pillow and other wheels
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       gcc \
       pkg-config \
       zlib1g-dev \
       libjpeg-dev \
       libfreetype6-dev \
       liblcms2-dev \
       libopenjp2-7-dev \
       libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

# copy only requirements first to leverage Docker cache
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r /app/requirements.txt

# copy project files from current build context (backend/)
COPY . /app

ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2"]
