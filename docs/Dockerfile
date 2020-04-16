FROM python:3.7.7-alpine3.11 as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

COPY piazza-api/dist/piazza_api-0.1.0-py3-none-any.whl /

RUN apk add --no-cache make && pip install -U pip && pip install sphinx && pip install pallets_sphinx_themes && pip install sphinxcontrib-katex && pip install piazza_api-0.1.0-py3-none-any.whl

WORKDIR docs
COPY docs /docs

RUN make html

FROM nginx:1.16-alpine

COPY --from=builder /docs/build/html /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]