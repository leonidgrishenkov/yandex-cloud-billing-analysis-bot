import aiosqlite

from bot import config


async def get_auth_users() -> list[int]:
    sql = """
        SELECT telegram_id
        FROM authusers
        WHERE 1=1
        AND is_active = 1
    """

    async with aiosqlite.connect(config.DB_PATH) as db:
        async with db.execute(sql) as cursor:
            return [row[0] async for row in cursor]
