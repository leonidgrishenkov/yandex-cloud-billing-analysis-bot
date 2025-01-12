# python:3.13.1-slim
# https://hub.docker.com/layers/library/python/3.13.1-slim/images/sha256-61c576c48c7324203bd8eee949d544910c406a0b7df7460522e3c3999c7f3b0f
FROM docker.io/python@sha256:1127090f9fff0b8e7c3a1367855ef8a3299472d2c9ed122948a576c39addeaf1

USER root

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -mU appuser -s /bin/bash
USER appuser

ENV HOME="/home/appuser"

WORKDIR $HOME/app

COPY --chown=appuser:appuser ./pyproject.toml ./uv.lock ./.env ./.yc-sa-auth.json $HOME/app/
COPY --chown=appuser:appuser ./bot $HOME/app/bot

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="$HOME/.local/bin:$PATH"

ENTRYPOINT ["uv", "run", "--no-dev", "--module", "bot", "--python", "$(which python3)", "--no-progress"]
