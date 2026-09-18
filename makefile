PYTHON := $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; elif command -v python3 >/dev/null 2>&1; then echo python3; elif command -v python >/dev/null 2>&1; then echo python; fi)

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
	@echo "Run: $(PYTHON) manage.py migrate"
	$(PYTHON) manage.py migrate

test:
	@echo "Run: $(PYTHON) manage.py test"
	$(PYTHON) manage.py test

create-admin:
	@if [ -n "$(username)" ] && [ -n "$(email)" ]; then \
		./create-admin.sh "$(username)" "$(email)"; \
	else \
		./create-admin.sh; \
	fi

run-server:
	@echo "Run: $(PYTHON) manage.py runserver"
	$(PYTHON) manage.py runserver

shell:
	@echo "Run: $(PYTHON) manage.py shell"
	$(PYTHON) manage.py shell

# snippets

startapp-snippets:
	@echo "Run: $(PYTHON) manage.py startapp snippets apps/snippets"
	$(PYTHON) manage.py startapp snippets apps/snippets

makemigrate-snippets:
	@echo "Run: $(PYTHON) manage.py makemigrations apps.snippets"
	$(PYTHON) manage.py makemigrations apps.snippets

migrate-snippets:
	@echo "Run: $(PYTHON) manage.py migrate apps.snippets"
	$(PYTHON) manage.py migrate apps.snippets

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
