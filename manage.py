#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # Set the default settings module for the 'django' program
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BINNY.settings")

    try:
        # Import Django's management commands
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If Django is not installed, raise an error
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable?"
        ) from exc

    # Execute the command passed to manage.py (e.g., `python manage.py runserver`)
    execute_from_command_line(sys.argv)
