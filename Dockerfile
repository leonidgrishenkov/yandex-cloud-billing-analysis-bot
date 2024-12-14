# 3.12.5-slim
# https://hub.docker.com/layers/library/python/3.12.5-slim/images/sha256-eac7a234d33269f362593c31d2ff1db7b116fbd794929f1f6015f5ea812ff254?context=explore
FROM docker.io/python@sha256:c24c34b502635f1f7c4e99dc09a2cbd85d480b7dcfd077198c6b5af138906390

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

COPY --chown=appuser:appuser ./pyproject.toml ./uv.lock ./.env $HOME/app/
COPY --chown=appuser:appuser ./bot $HOME/app/bot

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="$HOME/.local/bin:$PATH"

ENTRYPOINT ["uv", "run", "--no-dev", "--module", "bot", "--python", "$(which python3)", "--no-progress"]
