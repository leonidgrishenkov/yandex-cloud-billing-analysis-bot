from __future__ import annotations

import sqlite3
from datetime import date, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlite3 import Connection

from functools import singledispatch

from pandas import DataFrame, concat, read_sql

from bot import db, s3
from bot.config import REPORT_LIFETIME_THRESHOLD, S3_BUCKET_NAME, SQLITE_DB_FILE
from bot.logger import logger


@singledispatch
def get_fresh_report(report_date) -> DataFrame: ...


@get_fresh_report.register
def _get_fresh_report(report_date: date) -> DataFrame:
    logger.info("Trying to create fresh using s3 data")

    return s3.read_file(
        key=f'{report_date.strftime(r"%Y%m%d")}.csv',
        bucket=S3_BUCKET_NAME,
    )


@get_fresh_report.register
def _get_fresh_report(report_dates: list) -> DataFrame:
    logger.info("Trying to create fresh using s3 data")

    reports: list[DataFrame] = []
    for report_date in report_dates:
        try:
            reports.append(
                s3.read_file(
                    key=f'{report_date.strftime(r"%Y%m%d")}.csv',
                    bucket=S3_BUCKET_NAME,
                )
            )
        except FileNotFoundError as err:
            logger.warning("%s, skipping", err)
            continue
    return concat(reports)


def get_cached_report(dbtable: str, conn: Connection) -> DataFrame:
    logger.info("Reading report from cache using '%s' db table", dbtable)

    return read_sql(sql=f"SELECT * FROM {dbtable}", con=conn)


def cache_report(
    report: DataFrame, current_datetime: datetime, dbtable: str, conn: Connection
) -> ...:
    report["_created_at"] = current_datetime
    report.to_sql(name=dbtable, con=conn, if_exists="replace", index=False)

    logger.info("Cached report as '%s' db table", dbtable)


def create_report(report_date: list[date] | date, dbtable: str, current_datetime: datetime) -> DataFrame:
    conn = sqlite3.connect(SQLITE_DB_FILE)

    logger.info("Checking if '%s' table exists in '%s' sqlite db", dbtable, SQLITE_DB_FILE)
    if db.is_dbtable_exists(conn, dbtable):
        logger.info("'%s' table exists. Checking when it was created", dbtable)

        report_created_at: datetime = db.get_report_created_at(conn, dbtable)
        delta: float = (current_datetime - report_created_at).seconds

        if round(delta / (60 * 60), 0) <= REPORT_LIFETIME_THRESHOLD:
            logger.info(
                "Report created within %s hours at '%s'",
                REPORT_LIFETIME_THRESHOLD,
                report_created_at,
            )
            return get_cached_report(dbtable, conn)

        else:
            logger.info(
                "Report created later than %s hours",
                REPORT_LIFETIME_THRESHOLD,
            )
            report = get_fresh_report(report_date)
            cache_report(
                report=report, current_datetime=current_datetime, dbtable=dbtable, conn=conn
            )
            return report
    else:
        logger.info("'%s' table does not exists in db", dbtable)

        report = get_fresh_report(report_date)
        cache_report(report=report, current_datetime=current_datetime, dbtable=dbtable, conn=conn)
        return report
