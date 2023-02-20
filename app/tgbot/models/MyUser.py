import typing
from dataclasses import dataclass
from enum import Enum
from typing import Self, Any

from ordered_enum import OrderedEnum
from typeguard import typechecked, check_type

from app.tgbot.exseptions.exseptions import UserBuilderConvertError


# https://blog.yossarian.net/2020/03/02/Totally-ordered-enums-in-python-with-ordered_enum - more info
class Course(str, OrderedEnum):
    FIRST = "1 курс"  # 1 курс
    SECOND = "2 курс"  # 2 курс
    THIRD = "3 курс"  # 3 курс
    FOURTH = "4 курс"  # 4 курс
    MASTER = "Магистр"  # Магистр
    PHD = "Аспирант"  # Аспирант
    GRADUATE = "Выпускник"  # Выпускник


class Direction(str, Enum):
    KTiU = "КТиУ"
    TINT = "ТИНТ"
    NoZh = "НоЖ"
    FTMF = "ФТМФ"
    IVITSH = "ИВИТШ"
    IMRIP = "ИМРиП"
    FTMI = "ФТМИ"
    CPO = "ЦПО"
    VShTsK = "ВШЦК"
    OC_EIS = "ОЦ ЭИС"


class Interest(str, Enum):
    ART = "Искусство"  # Искусство, музыка и культура
    SCIENCE = "Наука"
    SPORT = "Спорт"
    MARKETING = "Маркетинг"
    ENTREPRENEURSHIP = "Предпринимательство"
    PROGRAMMING = "Программирование"
    PSYCHOLOGY = "Психология"
    TECHNOLOGIES = "Технологии"  # Технологии и инновации
    ECONOMY = "Финансы и экономика"
    TRIPS = "Путешествия и приключения"
    ECOLOGY = "Экология"
    POLICY = "Политика и экономика"
    PERSONAL_DEVELOPMENT = "Личное развитие"
    VOLUNTEERING = "Волонтерство"
    ML = "Машинное обучение"
    BLOCKCHAIN = "Blockchain"


class Sex(str, Enum):
    MEN = "Мужской",
    WOMEN = "Женский"


@dataclass(slots=True, frozen=True)
class MyUser:
    t_user_id: int
    email: str
    full_name: str
    sex: Sex
    user_name: str
    direction: Direction
    course: Course
    # interest: list[Interest]
    user_info: str
    ban: bool


class MyUserBuilder:
    t_user_id: int | None = None
    email: str | None = None
    full_name: str | None = None
    sex: Sex | None = None
    user_name: str | None = None
    direction: Direction | None = None
    course: Course | None = None
    user_info: str | None = None
    ban: bool = False

    @typechecked
    def set_t_user_id(self, t_user_id: int) -> Self:
        self.t_user_id = t_user_id
        return self

    @typechecked
    def set_email(self, email: str) -> Self:
        self.email = email
        return self

    @typechecked
    def set_full_name(self, full_name: str) -> Self:
        self.full_name = full_name
        return self

    @typechecked
    def set_sex(self, sex: Sex) -> Self:
        self.sex = sex
        return self

    @typechecked
    def set_user_name(self, user_name: str) -> Self:
        self.user_name = user_name
        return self

    @typechecked
    def set_direction(self, direction: Direction) -> Self:
        self.direction = direction
        return self

    @typechecked
    def set_course(self, course: Course) -> Self:
        self.course = course
        return self

    # @typechecked
    # def set_interest(self, interest: list[Interest]) -> Self:
    #     self.interest = interest
    #     return self

    @typechecked
    def set_user_info(self, user_info: str) -> Self:
        self.user_info = user_info
        return self

    @typechecked
    def set_ban(self, ban: bool) -> Self:
        self.ban = ban
        return self

    @typechecked
    def to_user(self) -> MyUser:
        if not (self.t_user_id and self.email and
                self.full_name and self.sex and
                self.user_name and self.direction and
                self.course and self.user_info):
            raise UserBuilderConvertError("Can't convert builder to user, because builder contain not set value")
        return MyUser(self.t_user_id, self.email,
                      self.full_name, self.sex,
                      self.user_name, self.direction,
                      self.course,
                      # self.interest,
                      self.user_info, self.ban)

    @staticmethod
    @typechecked
    def from_user(my_user: MyUser) -> Self:
        return MyUserBuilder() \
            .set_t_user_id(my_user.t_user_id) \
            .set_email(my_user.email) \
            .set_full_name(my_user.full_name) \
            .set_sex(my_user.sex) \
            .set_user_name(my_user.user_name) \
            .set_direction(my_user.direction) \
            .set_course(my_user.course) \
            .set_user_info(my_user.user_info) \
            .set_ban(my_user.ban)
        # .set_interest(my_user.interest)

    def to_dict(self) -> dict[str, Any]:
        return {
            't_user_id': self.t_user_id,
            'email': self.email,
            'full_name': self.full_name,
            'sex': self.sex,
            'user_name': self.user_name,
            'direction': self.direction,
            'course': self.course,
            'user_info': self.user_info,
            'ban': self.ban
        }

    @staticmethod
    @typechecked
    def from_dict(message: dict | None) -> Self | None:
        if not message:
            return None

        check_type('t_user_id', message['t_user_id'], int | None)
        check_type('email', message['email'], str | None)
        check_type('full_name', message['full_name'], str | None)
        check_type('sex', message['sex'], str | None)
        check_type('user_name', message['user_name'], str | None)
        check_type('direction', message['direction'], str | None)
        check_type('course', message['course'], str | None)
        check_type('user_info', message['user_info'], str | None)
        check_type('ban', message['ban'], bool)

        my_builder: MyUserBuilder = MyUserBuilder()

        t_user_id: int | None = typing.cast(int | None, message['t_user_id'])
        if t_user_id:
            my_builder.set_t_user_id(t_user_id)

        email: str | None = typing.cast(str | None, message['email'])
        if email:
            my_builder.set_email(email)

        full_name: str | None = typing.cast(str | None, message['full_name'])
        if full_name:
            my_builder.set_full_name(full_name)

        sex: Sex | None = typing.cast(str | None, message['sex'])
        if sex:
            my_builder.set_sex(Sex(sex))

        user_name: str | None = typing.cast(str | None, message['user_name'])
        if user_name:
            my_builder.set_user_name(user_name)

        direction: Direction | None = typing.cast(str | None, message['direction'])
        if direction:
            my_builder.set_direction(Direction(direction))

        course: Course | None = typing.cast(str | None, message['course'])
        if course:
            my_builder.set_course(Course(course))

        user_info: str | None = typing.cast(str | None, message['user_info'])
        if user_info:
            my_builder.set_user_info(user_info)

        ban: bool = typing.cast(bool, message['ban'])
        my_builder.set_ban(ban)

        return my_builder
