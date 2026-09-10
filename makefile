create:
	python3 -m venv .venv

active:
	@echo "Run: source .venv/bin/activate"

deactivate:
	@echo "Run: deactivate"

save-requirements:
	@echo "Run: pip freeze > requirements.txt"
	pip freeze > requirements.txt

install-requirements:
	@echo "Run: pip install -r requirements.txt"
	pip install -r requirements.txt

migrate:
	@echo "Run: python manage.py migrate"
	python manage.py migrate

create-admin:
	@echo "Run: python manage.py createsuperuser"
	python manage.py createsuperuser --username admin --email admin@example.com

run-server:
	@echo "Run: python manage.py runserver"
	python manage.py runserver

shell:
	@echo "Run: python manage.py shell"
	python manage.py shell

# snippets

startapp-snippets:
	@echo "Run: python manage.py startapp snippets apps/snippets"
	python manage.py startapp snippets apps/snippets

makemigrate-snippets:
	@echo "Run: python manage.py makemigrations apps.snippets"
	python manage.py makemigrations apps.snippets

migrate-snippets:
	@echo "Run: python manage.py migrate apps.snippets"
	python manage.py migrate apps.snippets
