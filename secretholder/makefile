start_db:
	docker compose up -d

install_uv:
    curl -LsSf https://astral.sh/uv/install.sh | sh

migrate:
	uv run migration.py

setup: start_db install_uv migrate

start:
	uv run src/main.py

stop_db:
	docker compose down

start_sso_server:
	uv run sso_server.py

build:
	docker compose up --build
