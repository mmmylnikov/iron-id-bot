FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /install

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock /install/

RUN uv sync --frozen --no-install-project --no-dev


FROM python:3.13-slim-bookworm

ENV LANG=ru_RU.UTF-8 \
    LC_ALL=ru_RU.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/deps/.venv/bin:$PATH"

WORKDIR /opt/app

COPY --chown=1000:1000 . /opt/app

COPY --from=builder /install /opt/deps

RUN apt-get update && apt-get install -y --no-install-recommends locales && \
    sed -i 's/# ru_RU.UTF-8/ru_RU.UTF-8/' /etc/locale.gen && \
    locale-gen ru_RU.UTF-8 && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

USER 1000

EXPOSE 8000

CMD ["python", "bot.py"]
