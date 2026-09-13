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

# docker
docker-build:
	@echo "Run: docker compose build"
	docker compose build

docker-up:
	@echo "Run: docker compose up -d"
	docker compose up -d

docker-logs:
	@echo "Run: docker compose logs -f"
	docker compose logs -f

docker-down:
	@echo "Run: docker compose down"
	docker compose down

docker-stop:
	@echo "Run: docker compose stop"
	docker compose stop

docker-restart:
	@echo "Run: docker compose restart"
	docker compose restart

docker-shell:
	@echo "Run: docker compose exec web bash"
	docker compose exec web bash
