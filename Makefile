lintformat:
	poetry run black .


loadtestcreate:
	poetry run locust -f locust/create-short-link.py --headless -u 20 -r 20 -t 30s


loadtestredirect:
	poetry run locust -f locust/redirect.py --headless -u 300 -r 300 -t 60s


stresstestcreate:
	poetry run locust -f locust/create-short-link.py --headless -u 100 -r 10 -t 30s


stresstestredirect:
	poetry run locust -f locust/redirect.py --headless -u 300 -r 30 -t 30s


unittest:
	poetry run pytest src/ -v -c pytest-unit.ini


integrationtest:
	TESTCONTAINERS_RYUK_DISABLED=true poetry run pytest src/ -v -c pytest-integration.ini


e2etest:
	TESTCONTAINERS_RYUK_DISABLED=true poetry run pytest src/ -v -c pytest-e2e.ini


initalembic:
	poetry run alembic init alembic


upgradelocal:
	poetry run alembic upgrade head


revisionlocal:
	poetry run alembic revision --autogenerate -m "$(m)"


startlocal:
	rm -rf .env || true
	cat docker/dev/env.example > .env
	docker compose -f docker/dev/docker-compose.yml up -d --build


stoplocal:
	docker compose -f docker/dev/docker-compose.yml down
	docker image prune -a -f
	docker volume prune -f
