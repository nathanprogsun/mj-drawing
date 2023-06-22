from enum import IntEnum


class UserState(IntEnum):
    registered = 1
    active = 2
    declined = 3  # Super Admin refused to activate user
    deactivated = 4  # Super Admin deactivated an active user
