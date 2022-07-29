FROM python:3.10-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

RUN apt update && apt install -y mariadb-client
WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.14

RUN apt install -y gcc libffi-dev g++ && pip install "poetry==$POETRY_VERSION"

COPY . .

RUN poetry install --no-dev --no-root && poetry build

FROM base as final

COPY --from=builder /app/dist /app/dist

ENV MARIADB_DRIVE_DUMP_CONFIG_DIR=/config/
RUN pip install /app/dist/*.whl
CMD ["python", "-m", "mariadb_drive_dump"]