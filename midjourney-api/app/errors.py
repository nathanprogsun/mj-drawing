from enum import IntEnum


class UserBizError(IntEnum):
    USER_NOT_FOUND = 11001


class DrawingBizError(IntEnum):
    NOT_SUPPORT_FILE_TYPE = 21001
    UPLOAD_ATTACHMENT_ERR = 21002
