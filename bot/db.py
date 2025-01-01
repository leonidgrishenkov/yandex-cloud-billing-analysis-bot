from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlite3 import Connection

def is_dbtable_exists(conn: Connection, dbtable: str) -> bool:
    cursor = conn.cursor()

    is_dbtable_exists = bool(
        cursor.execute(f"""
        SELECT
            EXISTS (
                SELECT 1
                FROM sqlite_master
                WHERE 1=1
                    AND name = '{dbtable}'
            );
    """).fetchone()[0]
    )
    cursor.close()

    return is_dbtable_exists


def get_report_created_at(conn: Connection, dbtable: str) -> datetime:
    cursor = conn.cursor()

    report_created_at: datetime = datetime.fromisoformat(
        cursor.execute(f"SELECT DISTINCT _created_at FROM {dbtable}").fetchone()[0]
    )
    cursor.close()

    return report_created_at
