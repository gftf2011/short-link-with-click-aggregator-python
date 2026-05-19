ARG PYTHON_VERSION=3.14

FROM python:${PYTHON_VERSION}-alpine AS builder

ENV POETRY_VERSION=2.3.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apk add --no-cache --virtual .build-deps \
        gcc musl-dev linux-headers libffi-dev \
    && pip install --no-cache-dir poetry==${POETRY_VERSION}

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY src ./src

RUN find ./src \( -name '*_test.py' -o -name '*_e2e_test.py' -o -name '*_integration_test.py' \) -delete \
    && poetry install --without dev --no-root --no-ansi \
    && .venv/bin/pip install --no-cache-dir "uvicorn" \
    && rm -rf "${POETRY_CACHE_DIR}" \
    && find .venv -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true \
    && find .venv -type f -name '*.pyc' -delete 2>/dev/null || true \
    && apk del .build-deps

FROM python:${PYTHON_VERSION}-alpine AS runtime

RUN addgroup -S app -g 1000 && adduser -S app -u 1000 -G app -s /sbin/nologin app

WORKDIR /app

COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app/src /app/src
COPY --chown=app:app alembic.ini /app/alembic.ini
COPY --chown=app:app alembic /app/alembic
COPY --chown=app:app scripts/create_short_link_partitions.py /app/scripts/create_short_link_partitions.py
COPY --chown=app:app docker/dev/api/entrypoint.sh /app/entrypoint.sh

ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src

RUN chmod +x /app/entrypoint.sh

USER app

EXPOSE 8000

CMD ["/app/entrypoint.sh"]
