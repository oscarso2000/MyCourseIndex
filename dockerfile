FROM node:12.16.1 as builder

WORKDIR /app

COPY client/package.json /app/
COPY client/yarn.lock /app/
RUN yarn install

COPY client /app/
WORKDIR client/
RUN yarn build

FROM python:3.7.6

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.0.2

RUN pip install -U pip
RUN pip install "poetry==$POETRY_VERSION"

# COPY poetry.lock .
# COPY pyproject.toml .

WORKDIR /app
COPY . /app
COPY --from=builder /app/build /app/client/build

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --no-dev --no-root

EXPOSE 5000

CMD ["python", "-m", "gunicorn.app.wsgiapp", "app:app", "-w 2", "-b 0.0.0.0:5000"]