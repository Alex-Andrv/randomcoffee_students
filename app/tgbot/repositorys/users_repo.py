from typing import List

from asyncpg import Connection, Record
from typeguard import check_type

from app.tgbot.models.MyUser import MyUser, Direction, Course, Sex


def _get_my_user(user: Record) -> MyUser | None:
    if not user:
        return None
    check_type('t_user_id', user['t_user_id'], int)
    check_type('email', user['email'], str)
    check_type('full_name', user['full_name'], str)
    check_type('sex', Sex(user['sex']), Sex)
    check_type('user_name', user['user_name'], str)
    check_type('direction', Direction(user['direction']), Direction)
    check_type('course', Course(user['course']), Course)
    check_type('user_info', user['user_info'], str)
    return MyUser(t_user_id=user['t_user_id'],
                  email=user['email'],
                  full_name=user['full_name'],
                  sex=Sex(user['sex']),
                  user_name=user['user_name'],
                  direction=Direction(user['direction']),
                  course=Course(user['course']),
                  user_info=user['user_info'])


def _get_my_users(users: list[Record]) -> List[MyUser]:
    return [_get_my_user(user) for user in users]


class UserRepo:
    """Db abstraction layer"""

    def __init__(self, conn: Connection):
        self.conn = conn

    async def get_by_email(self, email) -> MyUser | None:
        return _get_my_user(await self.conn.fetchrow('SELECT * FROM users WHERE email=$1', email))

    async def get_by_t_user_id(self, t_user_id) -> MyUser | None:
        return _get_my_user(await self.conn.fetchrow('SELECT * FROM users WHERE t_user_id=$1', t_user_id))

    async def upsert(self, my_user: MyUser) -> bool:
        return await self.conn.execute(
            """
            INSERT INTO users(
                t_user_id, user_name,
                email, full_name,
                direction, user_info,
                course, sex)
            VALUES($1,$2,$3,$4,$5,$6,$7,$8) ON CONFLICT(t_user_id) DO UPDATE SET
                (user_name, email, 
                full_name, direction, 
                user_info, course, 
                sex) 
                    = 
                (excluded.user_name,excluded.email,
                excluded.full_name,excluded.direction,
                excluded.user_info,excluded.course,
                excluded.sex);
            """,
            my_user.t_user_id, my_user.user_name,
            my_user.email, my_user.full_name,
            my_user.direction, my_user.user_info,
            my_user.course, my_user.sex) == 'INSERT 0 1'
