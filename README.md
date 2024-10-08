https://yandex.cloud/ru/docs/billing/operations/get-folder-report

```sh
python src/main.py
```

```sh
docker build -t billing-analysis:dev-2.0.0 -f Dockerfile .
```

```sh
docker run --rm \
    --name billing-analysis \
    billing-analysis:dev-2.0.0
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
