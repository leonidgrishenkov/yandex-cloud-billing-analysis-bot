import requests

from bot import config
from bot.logger import logger


class YandexCloudAPIError(Exception): ...


def get_balance() -> float:
    base_url = "https://billing.api.cloud.yandex.net/billing/v1/billingAccounts"

    logger.info(f"Requesting API to get billing account balance: {base_url}")

    response = requests.get(
        url=f"{base_url}/{config.YC_BILLING_ACC_ID}",
        headers={"Authorization": f"Bearer {config.YC_IAM_TOKEN}"},
    )
    response.raise_for_status()

    data = response.json()

    if "balance" in data.keys():
        balance = data["balance"]

        if not isinstance(balance, float):
            balance = float(balance)

        return balance
    else:
        raise YandexCloudAPIError("No `balance` key in API response")
