FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /srv

# Függőségek külön rétegben, hogy a Docker cache-elni tudja őket
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/

ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}
LABEL org.opencontainers.image.title="teendo-app" \
      org.opencontainers.image.version="${APP_VERSION}"

# Nem root felhasználóként futunk
RUN useradd --uid 10001 --no-create-home appuser
USER 10001

EXPOSE 8080

HEALTHCHECK --interval=15s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=2)" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "4", "--access-logfile", "-", "app:create_app()"]
