#!/usr/bin/env python
"""
Script to seed the database with test data.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to sys.path
current_path = Path(__file__).parent.resolve()
sys.path.append(str(current_path.parent))

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

import django

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()


def create_superuser():
    """
    Create a superuser if one doesn't exist.
    """
    if not User.objects.filter(email="admin@example.com").exists():
        User.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword",
            first_name="Admin",
            last_name="User",
        )
        print("Superuser created.")
    else:
        print("Superuser already exists.")


def create_test_users():
    """
    Create test users if they don't exist.
    """
    test_users = [
        {
            "email": "user1@example.com",
            "password": "userpassword",
            "first_name": "User",
            "last_name": "One",
        },
        {
            "email": "user2@example.com",
            "password": "userpassword",
            "first_name": "User",
            "last_name": "Two",
        },
        {
            "email": "user3@example.com",
            "password": "userpassword",
            "first_name": "User",
            "last_name": "Three",
        },
    ]
    
    for user_data in test_users:
        if not User.objects.filter(email=user_data["email"]).exists():
            User.objects.create_user(**user_data)
            print(f"Test user {user_data['email']} created.")
        else:
            print(f"Test user {user_data['email']} already exists.")


def main():
    """
    Main function to seed the database.
    """
    print("Seeding database...")
    create_superuser()
    create_test_users()
    print("Database seeding complete.")


if __name__ == "__main__":
    main()
