# Development Guide

This document provides guidelines and instructions for developing with the Django DRF Template.

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- Redis (optional, for caching and Celery)

### Setting Up the Development Environment

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/django-drf-template.git
   cd django-drf-template
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```
   pip install -r requirements/development.txt
   ```

4. Create a `.env` file from the example:
   ```
   cp .env.example .env
   ```

5. Edit the `.env` file to configure your environment variables.

6. Run migrations:
   ```
   python manage.py migrate
   ```

7. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```
   python manage.py runserver
   ```

### Using Docker for Development

1. Make sure Docker and Docker Compose are installed.

2. Create a `.env` file from the example:
   ```
   cp .env.example .env
   ```

3. Edit the `.env` file to configure your environment variables.

4. Build and start the containers:
   ```
   docker-compose -f docker-compose.dev.yml up -d --build
   ```

5. Run migrations:
   ```
   docker-compose -f docker-compose.dev.yml exec web python manage.py migrate
   ```

6. Create a superuser:
   ```
   docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
   ```

## Project Structure

The project follows a modular structure with separate apps for different functionalities:

- `config/`: Project configuration files
  - `settings/`: Environment-specific settings
  - `urls.py`: Main URL configuration
  - `wsgi.py` and `asgi.py`: WSGI and ASGI configurations

- `apps/`: Django applications
  - `core/`: Core functionality shared across apps
  - `users/`: User management
  - `authentication/`: Authentication functionality
  - `api/`: API-specific functionality

## Development Workflow

### Adding a New App

1. Create a new app in the `apps` directory:
   ```
   python manage.py startapp new_app apps/new_app
   ```

2. Add the app to `INSTALLED_APPS` in `config/settings/base.py`:
   ```python
   LOCAL_APPS = [
       # ...
       "apps.new_app",
   ]
   ```

3. Create the necessary files for the app:
   - `models.py`: Define your models
   - `serializers.py`: Define your serializers
   - `views.py`: Define your views
   - `urls.py`: Define your URLs
   - `tests/`: Add tests for your app

4. Include the app's URLs in `apps/api/urls.py`:
   ```python
   urlpatterns = [
       # ...
       path("new-app/", include("apps.new_app.urls")),
   ]
   ```

### Running Tests

Run tests with:

```
python manage.py test
```

Or with coverage:

```
coverage run --source='.' manage.py test
coverage report
```

### Code Quality

The project includes several tools for maintaining code quality:

- **Black**: Code formatter
  ```
  black .
  ```

- **isort**: Import sorter
  ```
  isort .
  ```

- **Flake8**: Linter
  ```
  flake8
  ```

- **mypy**: Type checker
  ```
  mypy .
  ```

## API Documentation

The API documentation is available at `/api/docs/` when the server is running. It is generated using Swagger/OpenAPI.

## Troubleshooting

### Common Issues

- **Database connection issues**: Make sure PostgreSQL is running and the connection details in `.env` are correct.
- **Migration errors**: Check if there are conflicting migrations or if the database schema is out of sync.
- **Import errors**: Make sure the virtual environment is activated and all dependencies are installed.

### Getting Help

If you encounter any issues, please check the project's issue tracker or create a new issue.
