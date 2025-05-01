#!/bin/bash

# Setup script for the Django DRF Template project
# This script will help you set up the project for development

# Exit on error
set -e

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Unix/Linux/MacOS
    source venv/bin/activate
fi

# Install development dependencies
echo "Installing development dependencies..."
pip install -r requirements/development.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env

    # Generate a random secret key
    SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(50))")

    # Replace the placeholder secret key in .env
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        sed -i "s/your-secret-key-here/$SECRET_KEY/g" .env
    else
        # Unix/Linux/MacOS
        sed -i '' "s/your-secret-key-here/$SECRET_KEY/g" .env
    fi
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create superuser if needed
echo "Do you want to create a superuser? (y/n)"
read -r create_superuser
if [[ "$create_superuser" =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Setup complete! You can now run the development server with:"
echo "python manage.py runserver"
