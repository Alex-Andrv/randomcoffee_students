from datetime import datetime

from asyncpg import Connection, Record
from typeguard import check_type

from app.tgbot.models.Criterion import Criterion
from app.tgbot.models.WaitingCompanion import WaitingCompanion


def _get_waiting_companion(param: Record) -> WaitingCompanion | None:
    if not param:
        return None
    check_type('id', param['id'], int)
    check_type('t_user_id', param['t_user_id'], int)
    check_type('time', param['time'], datetime)
    check_type('criterion', Criterion(param['criterion']), Criterion)
    check_type('status', param['status'], int | None)
    return WaitingCompanion(
        id=param['id'],
        t_user_id=param['t_user_id'],
        time=param['time'],
        criterion=Criterion(param['criterion']),
        status=param['status'])


def _get_waiting_companions(params: list[Record]) -> list[WaitingCompanion]:
    return [_get_waiting_companion(param) for param in params]


class WaitingCompanionRepo:
    """Db abstraction layer"""

    def __init__(self, conn: Connection):
        self.conn = conn

    async def get_by_criteria(self, criterion):
        return await self.conn.fetch(
            """
            SELECT * FROM waiting_companions WHERE criterion<>$1 and status IS NULL
            """, criterion)

    async def get_by_user_id_with_null_status(self, user_id):
        return await self.conn.fetchrow(
            """
            SELECT * FROM waiting_companions WHERE t_user_id=$1 and status IS NULL
            """, user_id)

    async def get_by_user_id_any_status(self, user_id):
        return await self.conn.fetchrow(
            """
            SELECT * FROM waiting_companions WHERE t_user_id=$1
            """, user_id)

    async def try_lock_user(self, user_id, companion_id):
        return await self.conn.execute(
            """
            UPDATE waiting_companions 
                SET status=$1 WHERE t_user_id=$2 and status IS NULL
            """, user_id, companion_id)

    async def try_unlock_user(self, user_id):
        return await self.conn.execute(
            """
            UPDATE waiting_companions 
            SET status=NULL WHERE t_user_id=$1
            """, user_id)

    async def add_waiting_companion(self, user_id: int, criterion: str):
        return await self.conn.execute(
            """
            INSERT INTO waiting_companions (
            t_user_id, time, criterion) 
            VALUES ($1,now(),$2)
            """,
            user_id, criterion)

    # only for tests
    async def get_all_data(self):
        return await self.conn.fetch(
            """
            SELECT * FROM waiting_companions
            """)

    async def delete_request_for_t_user_id_with_null_status(self, t_user_id: int) -> bool:
        return await self.conn.execute(
            """
            DELETE FROM waiting_companions 
               WHERE t_user_id=$1 AND status is NULL
            """, t_user_id) == 'DELETE 1'

    async def get_users_by_waiting_id(self, waiting_id) -> WaitingCompanion:
        return _get_waiting_companion(await self.conn.fetchrow("""
        SELECT * FROM waiting_companions WHERE id=$1
        """, waiting_id))

    async def get_strangers(self, t_user_id: int) -> list[WaitingCompanion]:
        return _get_waiting_companions(await self.conn.fetch(
            """SELECT * FROM waiting_companions as wc WHERE status IS NULL AND NOT EXISTS(
            SELECT 1 
            FROM 
               (SELECT waiting_id, t_user_id FROM meetings as f WHERE f.t_user_id = $1) first 
            INNER JOIN 
               (SELECT waiting_id, t_user_id FROM meetings as s WHERE s.t_user_id = wc.t_user_id) second USING(waiting_id) 
            WHERE first.t_user_id <> second.t_user_id)""", t_user_id))
