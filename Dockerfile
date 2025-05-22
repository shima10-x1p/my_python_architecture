FROM ghcr.io/astral-sh/uv:python3.12-bookworm AS builder
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev

FROM python:3.12-slim-bookworm
WORKDIR /app
RUN python -m venv .venv --without-pip
COPY --from=builder /app/.venv/bin/uvicorn /app/.venv/bin/uvicorn
COPY --from=builder /app/.venv/lib/python3.12/site-packages /app/.venv/lib/python3.12/site-packages
COPY ./openapi_server /app/openapi_server
EXPOSE 8000
CMD ["/app/.venv/bin/uvicorn", "openapi_server.main:app", "--host", "0.0.0.0", "--port", "8080"]