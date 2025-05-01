# Deployment Guide

This document provides instructions for deploying the Django DRF Template to production environments.

## Prerequisites

- Docker and Docker Compose
- A domain name (for production deployments)
- SSL certificates (for HTTPS)

## Deployment Options

### Docker Deployment

The recommended way to deploy the application is using Docker and Docker Compose.

1. Clone the repository on your server:
   ```
   git clone https://github.com/yourusername/django-drf-template.git
   cd django-drf-template
   ```

2. Create a `.env` file from the example and configure it for production:
   ```
   cp .env.example .env
   ```

3. Edit the `.env` file to set production values:
   ```
   DEBUG=False
   SECRET_KEY=your-secure-secret-key
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   DATABASE_URL=postgres://user:password@db:5432/dbname
   ```

4. Generate SSL certificates or copy your existing ones to `docker/nginx/certs/`:
   ```
   mkdir -p docker/nginx/certs
   # Copy your SSL certificates here
   cp /path/to/your/certificate.crt docker/nginx/certs/server.crt
   cp /path/to/your/private.key docker/nginx/certs/server.key
   ```

5. Build and start the containers:
   ```
   docker-compose up -d --build
   ```

6. Run migrations:
   ```
   docker-compose exec web python manage.py migrate
   ```

7. Create a superuser:
   ```
   docker-compose exec web python manage.py createsuperuser
   ```

8. Collect static files:
   ```
   docker-compose exec web python manage.py collectstatic --noinput
   ```

### Manual Deployment

If you prefer to deploy without Docker, follow these steps:

1. Set up a server with Python 3.8+, PostgreSQL, and Nginx.

2. Clone the repository:
   ```
   git clone https://github.com/yourusername/django-drf-template.git
   cd django-drf-template
   ```

3. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

4. Install production dependencies:
   ```
   pip install -r requirements/production.txt
   ```

5. Create a `.env` file and configure it for production.

6. Run migrations:
   ```
   python manage.py migrate
   ```

7. Collect static files:
   ```
   python manage.py collectstatic --noinput
   ```

8. Set up Gunicorn as a systemd service.

9. Configure Nginx as a reverse proxy.

## Environment Variables

The following environment variables should be set in production:

- `DEBUG`: Set to `False` in production
- `SECRET_KEY`: A secure secret key
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection URL
- `REDIS_URL`: Redis connection URL (if using Redis)
- `EMAIL_*`: Email configuration
- `SENTRY_DSN`: Sentry DSN for error tracking (optional)
- `AWS_*`: AWS configuration (if using S3 for storage)

## Security Considerations

1. **SSL/TLS**: Always use HTTPS in production. The Docker setup includes Nginx with SSL configuration.

2. **Secret Key**: Use a strong, unique secret key in production and keep it secret.

3. **Debug Mode**: Ensure `DEBUG` is set to `False` in production.

4. **Database**: Use a strong password for the database and restrict access to it.

5. **Environment Variables**: Store sensitive information in environment variables, not in code.

6. **Regular Updates**: Keep dependencies updated to patch security vulnerabilities.

## Monitoring and Maintenance

1. **Logging**: Configure logging to monitor application behavior.

2. **Backups**: Regularly backup the database and media files.

3. **Updates**: Regularly update dependencies and apply security patches.

4. **Monitoring**: Use tools like Sentry for error tracking and Prometheus for metrics.

## Scaling

1. **Horizontal Scaling**: Add more web containers behind a load balancer.

2. **Database Scaling**: Consider read replicas or sharding for database scaling.

3. **Caching**: Implement Redis caching for frequently accessed data.

4. **CDN**: Use a CDN for static and media files.

## Troubleshooting

### Common Issues

- **502 Bad Gateway**: Check if Gunicorn is running and Nginx configuration is correct.
- **Database Connection Issues**: Verify database credentials and network connectivity.
- **Static Files Not Loading**: Check if static files are collected and Nginx is configured to serve them.

### Checking Logs

```
docker-compose logs web  # Check web container logs
docker-compose logs nginx  # Check Nginx logs
```

## Rollback Procedure

If a deployment fails, follow these steps to rollback:

1. Identify the last working version.

2. Stop the current containers:
   ```
   docker-compose down
   ```

3. Checkout the last working version:
   ```
   git checkout <last-working-commit>
   ```

4. Rebuild and start the containers:
   ```
   docker-compose up -d --build
   ```

5. Run migrations if necessary:
   ```
   docker-compose exec web python manage.py migrate
   ```
