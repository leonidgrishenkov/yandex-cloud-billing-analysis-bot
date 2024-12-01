# 3.12.5-slim
# https://hub.docker.com/layers/library/python/3.12.5-slim/images/sha256-eac7a234d33269f362593c31d2ff1db7b116fbd794929f1f6015f5ea812ff254?context=explore
FROM docker.io/python@sha256:c24c34b502635f1f7c4e99dc09a2cbd85d480b7dcfd077198c6b5af138906390

USER root
WORKDIR /app

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install poetry.
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry $(which python3) -

ENV PATH="/opt/poetry/bin:$PATH"

COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock
COPY ./.env /app/.env
COPY ./bot /app/bot

# Create virtual environment and install all dependencies.
RUN cd /app \
    && poetry env use $(which python3) \
    && poetry install --without=dev

ENTRYPOINT ["poetry", "run", "python", "-m", "bot"]
