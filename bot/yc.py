from __future__ import annotations

import json
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Self
from zoneinfo import ZoneInfo

import jwt
import requests
from pydantic import BaseModel, Field, model_validator

from bot import db
from bot.config import SQLITE_DB_FILE, YC_BILLING_ACC_ID, YC_SA_AUTH_JSON
from bot.logger import logger

if TYPE_CHECKING:
    from sqlite3 import Connection


class BillingAccountBalance(BaseModel):
    active: bool
    id: str
    name: str
    createdAt: str
    countryCode: str
    currency: str
    balance: float



class IAMToken(BaseModel):
    token: str = Field(..., alias="iamToken", repr=False)
    expires_at: str = Field(..., alias="expiresAt")
    expires_at_dttm: Optional[datetime] = None

    @model_validator(mode="after")
    def set_expires_at_dttm(self) -> Self:
        try:
            self.expires_at_dttm = datetime.fromisoformat(self.expires_at).astimezone(
                ZoneInfo("Europe/Moscow")
            )
        except ValueError:
            raise ValueError(f"Invalid ISO 8601 datetime string: {self.expires_at}")
        return self


class AuthKey(BaseModel):
    id: str
    service_account_id: str
    created_at: str
    key_algorithm: str
    private_key: str = Field(..., repr=False)
    public_key: str = Field(..., repr=False)

    @classmethod
    def from_json(cls, path: Path) -> Self:
        return cls(**json.loads(path.read_text()))


def _get_iam_token(url: str, dbtable: str, dbfile: Path, authkey_path: Path) -> IAMToken:
    """Get active IAM token from cache or Yandex Cloud API.

    Args:
        url: API url to request IAM token
        dbtable: Table name in sqlite3 database
        dbfile: Sqlite3 database file
        authkey_path: Service account auth key path

    Returns:
        IAM token
    """
    current_datetime: datetime = datetime.now().astimezone(ZoneInfo("Europe/Moscow"))

    conn = sqlite3.connect(dbfile)
    conn.row_factory = sqlite3.Row

    logger.info("Checking if '%s' table exists in '%s' sqlite db", dbtable, dbfile)
    if db.is_dbtable_exists(conn, dbtable):
        logger.info("'%s' table exists", dbtable)

        cursor = conn.cursor()

        row = cursor.execute(f"""
            SELECT
                token, expires_at, expires_at_dttm
            FROM {dbtable}
        """).fetchone()
        row = dict(row)

        token = IAMToken(iamToken=row["token"], expiresAt=row["expires_at"])
        logger.debug("Recieved token %s", token)

        if current_datetime > token.expires_at_dttm:  # pyright: ignore[reportOperatorIssue]
            logger.info("Token expired")
            token = _request_new_iam_token(url, AuthKey.from_json(authkey_path))
        else:
            logger.info("Token is valid")
            conn.close()
            return token
    else:
        logger.info("Table does not exist")
        token = _request_new_iam_token(url, AuthKey.from_json(authkey_path))

    _dump_iam_token_into_db(token, dbtable, conn)
    conn.close()

    return token


def _request_new_iam_token(url: str, authkey: AuthKey) -> IAMToken:
    """Request new IAM Token via Yandex Cloud API.

    Args:
        url: Base API url
        authkey: Service account auth key

    Returns:
        New IAM token object.
    """
    logger.info("Getting new IAM token using url: %s", url)

    now = int(time.time())
    encoded_jwt = jwt.encode(
        payload={
            "aud": url,
            "iss": authkey.service_account_id,
            "iat": now,
            "exp": now + 3600,
        },
        key=authkey.private_key,
        algorithm="PS256",
        headers={"kid": authkey.id},
    )

    logger.debug("Sending request")
    response = requests.post(
        url=url,
        json={"jwt": encoded_jwt},
    )
    logger.debug("Response recieved")
    response.raise_for_status()

    return IAMToken(**response.json())


def _dump_iam_token_into_db(token: IAMToken, dbtable: str, conn: Connection) -> None:
    """Cache token into sqlite3 database.

    Args:
        token: IAM token
        dbtable: Database table name
        conn: Active sqlite3 connection
    """
    logger.info("Dumping token into db as '%s' table", dbtable)
    _token: dict = token.model_dump()

    cursor = conn.cursor()

    if db.is_dbtable_exists(conn, dbtable):
        logger.debug("Table '%s' already exists, dropping", dbtable)
        cursor.execute(f"DROP TABLE {dbtable}")

    ddl = f"""
        CREATE TABLE {dbtable}
        (
            token TEXT,
            expires_at TEXT,
            expires_at_dttm TIMESTAMP
        );
    """
    logger.debug("Creating table using query:\n %s", ddl)
    cursor.execute(ddl)

    columns = ", ".join(_token.keys())
    placeholders = ", ".join("?" for _ in _token)

    query = f"INSERT INTO {dbtable} ({columns}) VALUES ({placeholders})"
    logger.debug("Inserting data using query:\n %s", query)
    cursor.execute(query, tuple(_token.values()))

    conn.commit()


def get_balance() -> float:
    """Get current billing account balance."""

    base_url = "https://billing.api.cloud.yandex.net/billing/v1/billingAccounts"
    full_url = f"{base_url}/{YC_BILLING_ACC_ID}"

    logger.info(
        "Sending request to the API to get billing account balance using url: %s", {base_url}
    )
    iamtoken = _get_iam_token(
        url="https://iam.api.cloud.yandex.net/iam/v1/tokens",
        dbtable="iam_token",
        dbfile=SQLITE_DB_FILE,
        authkey_path=YC_SA_AUTH_JSON,
    )

    response = requests.get(
        url=full_url,
        headers={"Authorization": f"Bearer {iamtoken.token}"},
    )
    return BillingAccountBalance(**response.json()).balance
