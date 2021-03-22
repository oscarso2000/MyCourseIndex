FROM node:12.16-alpine3.11 as builder

WORKDIR /app

COPY client/package.json client/yarn.lock /app/
COPY client /app/
RUN yarn install && yarn build

###############################################################################
FROM python:3.7.7-slim-buster

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.4

RUN pip install -U pip && pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
COPY piazza-api/dist/piazza_api-0.1.0-py3-none-any.whl /app/piazza-api/dist/
RUN apt-get update -y && apt-get install -y gcc g++
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-dev --no-root && python -m spacy download en_core_web_lg && python -m spacy download en

COPY --from=builder /app/build /app/client/build

COPY app.py /app
COPY app /app/app
COPY concept_matching /app/concept_matching/

RUN python concept_matching/install_quickdb.py

# DEV ONLY
# COPY secrets /app/secrets


EXPOSE 5000

CMD ["python", "-m", "gunicorn.app.wsgiapp", "app:app", "-w 2", "-b 0.0.0.0:5000", "--log-level", "DEBUG", "--timeout", "3600"]