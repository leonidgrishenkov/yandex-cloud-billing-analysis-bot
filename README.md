https://yandex.cloud/ru/docs/billing/operations/get-folder-report

```sh
python src/main.py
```

```sh
docker build -t billing-analysis:dev-2.0.0 -f Dockerfile .
```


```sh
docker run --detach --rm \
    --name billing-analysis \
    -v ./pyproject.toml:/app/pyproject.toml \
    -v ./.env:/app/.env \
    -v ./src:/app/src \
    billing-analysis:dev-1.0.0 tail -f /dev/null
```

```sh
docker exec -it billing-analysis /bin/bash
```

```sh
poetry env use $(which python3)
```

```sh
. $(poetry env info --path)/bin/activate
```

```sh
poetry install
```

# yandex cloud

https://yandex.cloud/en-ru/docs/iam/concepts/authorization/oauth-token

https://yandex.cloud/en/docs/container-registry/operations/authentication

https://habr.com/ru/articles/697206/

YC_OAUTH_TOKEN

```sh
export YC_OAUTH_TOKEN=
```

```sh
echo $YC_OAUTH_TOKEN | docker login --username oauth --password-stdin cr.yandex
```

```sh
yc container registry list
```

# github actions

add YC_OAUTH_TOKEN, YC_REGISTRY_ID

repo > settings > secrets and variables > new repository secret

# Deploy vm on yandex cloud

```sh
cd ./deploy
```

```sh
source env.sh
```
