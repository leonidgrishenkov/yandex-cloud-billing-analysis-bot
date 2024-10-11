# About

[Getting expense details by folder | Yandex Cloud](https://yandex.cloud/ru/docs/billing/operations/get-folder-report).

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

```sh
docker logs -f yandex-cloud-billing-analysis-bot
```

# Deploy virtual machine on Yandex Cloud

The bot will run in docker container on virtual machine based on container optimazied image.

I deployed VM using Terraform.

```sh
cd ./deploy
```

```sh
source env.sh
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
