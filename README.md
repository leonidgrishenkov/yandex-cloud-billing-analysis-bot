https://yandex.cloud/ru/docs/billing/operations/get-folder-report

```sh
python src/main.py
```

```sh
docker build -t billing-analysis:dev-1.0.0 -f Dockerfile .
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
