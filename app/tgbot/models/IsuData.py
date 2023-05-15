from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class IsuData:
    t_user_id: int
    sub: str
    gender: str
    name: str
    isu: str | None
    preferred_username: str
    given_name: str
    middle_name: str | None
    family_name: str
    email: str
    email_verified: bool

