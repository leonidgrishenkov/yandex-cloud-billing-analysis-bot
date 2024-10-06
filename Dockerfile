FROM docker.io/python@sha256:c24c34b502635f1f7c4e99dc09a2cbd85d480b7dcfd077198c6b5af138906390

USER root
WORKDIR /app

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry $(which python3) -

ENV PATH="/opt/poetry/bin:$PATH"

# COPY ./pyproject.toml /app/pyproject.toml
# COPY ./.env /app/.env

# RUN cd /app \
#     && poetry env use $(which python3) \
#     && . $(poetry env info --path)/bin/activate \
#     && poetry install --only generator
