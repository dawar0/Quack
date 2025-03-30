FROM node:20-slim AS frontend-build

WORKDIR /frontend

# Copy package.json and install dependencies
COPY frontend/package*.json ./
RUN npm ci

# Copy frontend source code and build
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim

WORKDIR /app

# Install Nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Setup Nginx
COPY --from=frontend-build /frontend/dist /var/www/html
COPY deployment/nginx.conf /etc/nginx/sites-available/default

# Copy backend requirements and install
COPY backend/requirements.txt backend/pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy backend source code
COPY backend/ ./

# Copy startup script
COPY deployment/startup.sh /startup.sh
RUN chmod +x /startup.sh

# Set environment variables
ENV FLASK_APP=manage.py
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Expose the container port
EXPOSE 8080

# Run the start script
CMD ["/startup.sh"] 