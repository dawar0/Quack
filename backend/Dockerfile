FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=manage.py
ENV PYTHONUNBUFFERED=1

# Run migrations and start the application with gunicorn
CMD flask db upgrade && gunicorn --bind 0.0.0.0:8080 'app:create_app()' 