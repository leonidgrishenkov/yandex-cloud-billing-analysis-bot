<div align="center">
  <a href="https://github.com/leonidgrishenkov/yandex-cloud-billing-analysis-bot/actions/workflows/main.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/leonidgrishenkov/yandex-cloud-billing-analysis-bot/main.yml?style=flat-square&logo=github&logoColor=c7c7c7&label=CI&labelColor=282828&color=347D39&event=push" alt="CI status" />
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
  </a>
  <a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="UV">
  </a>
</div>

# About

[Getting expense details by folder | Yandex Cloud](https://yandex.cloud/ru/docs/billing/operations/get-folder-report).

[Watch the Bot usage demo video](https://youtu.be/wenye9Q32xo)

## Bot commands



# Local development

Build and run the bot inside docker container.

```sh
export IMAGE=yandex-cloud-billing-analysis-bot:dev-1.0.0
```

```sh
docker build -t $IMAGE -f Dockerfile .
```

```sh
docker run --detach --rm \
    --name yandex-cloud-billing-analysis-bot \
    $IMAGE
```

Get container logs:

```sh
docker logs -f yandex-cloud-billing-analysis-bot
```

Enter into container by `root` user:

```sh
docker exec -it -u root yandex-cloud-billing-analysis-bot /bin/bash
```

# Users authorization

Telegram users that can communicate with this bot should be set via `AUTH_USERS` env variable in `.env` file.

For multiple users use this format:

```sh
AUTH_USERS=1111,2222,3333,4444
```

For all required env variables see `.env.example`.

# Deploy virtual machine on Yandex Cloud

The bot will run in docker container on virtual machine based on container optimazied image.

I deployed VM using Terraform.

```sh
cd ./deploy
```

Allow `direnv` to load environment variables from `.envrc`:

```sh
direnv allow
```

Initialize terraform:

```sh
terraform init
```

Validate configurations:

```sh
terraform validate
```

Deploy:

```sh
terraform apply
```

Terraform output countains usefull informations, such as virtual machine public IP address and user password.

To show terraform output:

```sh
terraform output
```

Or in JSON format:

```sh
terraform output -json
```

# TODO

- [ ] Add handler to get report for the particular date
- [ ] Add background job that will send message when balance goes below specified threshold
- [x] Add report results caching
