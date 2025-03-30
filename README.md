# Quack Application

## Local Development with Docker Compose

You can run the entire application stack locally using Docker Compose:

```bash
# Build and start all services
docker-compose up --build

# Access the application at http://localhost
```

## Deploying to Google Cloud Run

### Prerequisites

1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. Initialize the SDK and login:
   ```
   gcloud init
   gcloud auth login
   ```

### Setting up Cloud Resources

1. Create a Cloud SQL PostgreSQL instance:
   ```
   gcloud sql instances create quack-db \
     --database-version=POSTGRES_16 \
     --tier=db-f1-micro \
     --region=us-central1 \
     --root-password=YOUR_PASSWORD
   ```

2. Create a database:
   ```
   gcloud sql databases create quack --instance=quack-db
   ```

3. Create a Redis instance using Memorystore:
   ```
   gcloud redis instances create quack-redis \
     --size=1 \
     --region=us-central1 \
     --tier=basic
   ```

4. Get connection information:
   ```
   REDIS_HOST=$(gcloud redis instances describe quack-redis --region=us-central1 --format='value(host)')
   REDIS_PORT=$(gcloud redis instances describe quack-redis --region=us-central1 --format='value(port)')
   ```

### Building and Deploying the Container

1. Build the container:
   ```
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/quack-app
   ```

2. Deploy to Cloud Run:
   ```
   gcloud run deploy quack \
     --image gcr.io/YOUR_PROJECT_ID/quack-app \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --add-cloudsql-instances YOUR_PROJECT_ID:us-central1:quack-db \
     --set-env-vars="DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@/quack?host=/cloudsql/YOUR_PROJECT_ID:us-central1:quack-db,REDIS_HOST=$REDIS_HOST,REDIS_PORT=$REDIS_PORT"
   ```

3. After deployment, you can access your application at the URL provided by Cloud Run.

## Configuration

The application can be configured using the following environment variables:

- `DATABASE_URL` - PostgreSQL connection URL
- `REDIS_HOST` - Redis host
- `REDIS_PORT` - Redis port
- `MAIL_SERVER` - SMTP server for emails
- `MAIL_PORT` - SMTP port
- `MAIL_USE_TLS` - Use TLS for mail (True/False)
- `MAIL_USERNAME` - SMTP username
- `MAIL_PASSWORD` - SMTP password
- `MAIL_DEFAULT_SENDER` - Default sender email

## Security Notes

- For production, ensure you're using secure passwords and proper IAM permissions
- Consider using Secret Manager for sensitive information like database passwords
- Enable VPC Service Controls for additional security 