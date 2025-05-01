# Setup script for the Django DRF Template project
# This script will help you set up the project for development on Windows

# Create virtual environment if it doesn't exist
if (-not (Test-Path -Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
& .\venv\Scripts\Activate.ps1

# Install development dependencies
Write-Host "Installing development dependencies..."
pip install -r requirements/development.txt

# Create .env file if it doesn't exist
if (-not (Test-Path -Path ".env")) {
    Write-Host "Creating .env file from .env.example..."
    Copy-Item -Path ".env.example" -Destination ".env"

    # Generate a random secret key
    $SECRET_KEY = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

    # Replace the placeholder secret key in .env
    (Get-Content -Path ".env") -replace "your-secret-key-here", $SECRET_KEY | Set-Content -Path ".env"
}

# Run migrations
Write-Host "Running migrations..."
python manage.py migrate

# Create superuser if needed
$create_superuser = Read-Host "Do you want to create a superuser? (y/n)"
if ($create_superuser -eq "y" -or $create_superuser -eq "Y") {
    python manage.py createsuperuser
}

# Collect static files
Write-Host "Collecting static files..."
python manage.py collectstatic --noinput

Write-Host "Setup complete! You can now run the development server with:"
Write-Host "python manage.py runserver"
