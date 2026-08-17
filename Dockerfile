# 1. Base Image: Slim debian-based Python image for minimal attack surface and size
FROM python:3.11-slim

# 2. Environment Variables: Prevent Python from buffering stdout/stderr & writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    APP_VERSION=1.0.0

# 3. Set working directory
WORKDIR /app

# 4. Install dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY . .

# 6. Security: Create a non-root user and switch to it
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 7. Expose internal port
EXPOSE 5000

# 8. Run via Gunicorn (2-4 workers standard for containerized web apps)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
