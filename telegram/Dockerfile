# Примерный Dockerfile

FROM python:3.13-slim

WORKDIR /telegram

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV PATH="/.venv/bin:$PATH"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync

ENV PYTHONPATH=/telegram

COPY ./* /telegram
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

CMD [ "./.venv/bin/python", "main.py" ]
