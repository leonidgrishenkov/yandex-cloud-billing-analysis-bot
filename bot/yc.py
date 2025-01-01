import os
from http import HTTPStatus

import requests

from bot import config
from bot.logger import logger


class YandexCloudAPIError(Exception): ...


def _get_iam_token():
    url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    logger.info(f"Sending request to get new IAM token: {url}")

    response = requests.post(
        url=url,
        json={"yandexPassportOauthToken": config.YC_OAUTH_TOKEN},
    )
    response.raise_for_status()

    data = response.json()
    iam_token: str = data["iamToken"]

    os.environ["YC_IAM_TOKEN"] = iam_token
    logger.info("Successfully set token as `YC_IAM_TOKEN` environment variable")


def get_balance() -> float:
    base_url = "https://billing.api.cloud.yandex.net/billing/v1/billingAccounts"
    full_url = f"{base_url}/{config.YC_BILLING_ACC_ID}"

    logger.info(f"Sending request to the API to get billing account balance: {base_url}")

    iam_token = os.getenv("YC_IAM_TOKEN")
    if not iam_token:
        logger.warning("`YC_IAM_TOKEN` variables not set, trying to get new token")
        _get_iam_token()
        iam_token = os.getenv("YC_IAM_TOKEN")

    try:
        response = requests.get(
            url=full_url,
            headers={"Authorization": f"Bearer {iam_token}"},
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            logger.warning(
                f"API returned {HTTPStatus.UNAUTHORIZED} status code, trying to get new IAM token. "
                f"Error message: {err}"
            )
            _get_iam_token()
            iam_token = os.getenv("YC_IAM_TOKEN")

            try:
                response = requests.get(
                    url=full_url,
                    headers={"Authorization": f"Bearer {iam_token}"},
                )
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                if response.status_code == HTTPStatus.UNAUTHORIZED:
                    logger.fatal(f"Got {HTTPStatus.UNAUTHORIZED} status code after second try")
                    raise err
                else:
                    raise err
        else:
            raise err

    data = response.json()
    logger.info(f"Response recieved. Keys: {list(data.keys())}")

    if "balance" in data.keys():
        balance = data["balance"]

        if not isinstance(balance, float):
            balance = float(balance)

        return balance
    else:
        raise YandexCloudAPIError("No `balance` key in API response")
