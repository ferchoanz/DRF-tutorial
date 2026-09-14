#!/bin/bash

set -euo pipefail

if [ -x ".venv/bin/python" ]; then
    PYTHON=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON="python"
else
    echo "Error: Python not found."
    exit 1
fi

USERNAME="${1:-}"
EMAIL="${2:-}"

if [ -z "$USERNAME" ]; then
    read -rp "Username: " USERNAME
fi

if [ -z "$EMAIL" ]; then
    read -rp "Email: " EMAIL
fi

if [ -z "$USERNAME" ] || [ -z "$EMAIL" ]; then
    echo "Error: username and email are required."
    echo "Usage: $0 <username> <email>"
    exit 1
fi

user_exists=$($PYTHON manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(username='${USERNAME}').exists())" 2>/dev/null | tail -1)
email_exists=$($PYTHON manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(email='${EMAIL}').exists())" 2>/dev/null | tail -1)

if [ "$user_exists" = "True" ]; then
    echo "Error: a user with username '$USERNAME' already exists."
    exit 1
fi

if [ "$email_exists" = "True" ]; then
    echo "Error: a user with email '$EMAIL' already exists."
    exit 1
fi

echo "Creating superuser '$USERNAME'..."
if [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
    $PYTHON manage.py createsuperuser --username "$USERNAME" --email "$EMAIL" --noinput
else
    $PYTHON manage.py createsuperuser --username "$USERNAME" --email "$EMAIL"
fi
