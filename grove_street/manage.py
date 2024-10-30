#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

import dotenv


def main():
    """Run administrative tasks."""

    # Read .env file from root of the project (or develop file first if it exists)
    env_paths = ["../.env.dev", "../.env"]
    for env_path in env_paths:
        if (path := Path(os.path.abspath(env_path))).exists():
            dotenv.read_dotenv(path)
            break

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grove_street.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
