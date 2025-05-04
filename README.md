# Django REST Framework Template

A professional, reusable Django REST Framework template for building scalable and maintainable APIs.

## Features

-   Modular app structure with clear separation of concerns
-   Custom user model with authentication system
-   JWT authentication
-   Standardized API response formatting
-   Environment-based configuration
-   Docker setup for development and production
-   Comprehensive test setup
-   API documentation with drf-spectacular (Swagger/OpenAPI)
-   Logging and monitoring
-   Security best practices

## Project Structure

```
django-drf-template/
│
├── .github/                          # GitHub specific files
├── config/                           # Project configuration
├── apps/                             # Django applications
│   ├── core/                         # Core functionality shared across apps
│   ├── users/                        # User management app
│   ├── authentication/               # Authentication app
│   └── api/                          # Main API app
├── templates/                        # HTML templates (if needed)
├── static/                           # Static files
├── media/                            # User-uploaded files
├── docs/                             # Project documentation
├── scripts/                          # Utility scripts
├── requirements/                     # Python dependencies
└── docker/                           # Docker configuration
```

## Getting Started

### Prerequisites

-   Python 3.8+
-   PostgreSQL
-   Docker and Docker Compose (optional)

### Installation

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

3. Install dependencies:

    ```
    pip install -r requirements/development.txt
    ```

4. Create a `.env` file from the example:

    ```
    cp .env.example .env
    ```

5. Run migrations:

    ```
    python manage.py migrate
    ```

6. Create a superuser:

    ```
    python manage.py createsuperuser
    ```

7. Run the development server:
    ```
    python manage.py runserver
    ```

### Using Docker

1. Build and start the containers:

    ```
    docker-compose up -d --build
    ```

2. Run migrations:

    ```
    docker-compose exec web python manage.py migrate
    ```

3. Create a superuser:
    ```
    docker-compose exec web python manage.py createsuperuser
    ```

## API Documentation

API documentation is available at `/api/docs/` when the server is running.

## Testing

Run tests with:

```
python manage.py test
```

Or with coverage:

```
coverage run --source='.' manage.py test
coverage report
```

## Deployment

See the deployment guide in the `docs/deployment/` directory for detailed instructions.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
