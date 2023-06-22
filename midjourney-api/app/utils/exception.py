import enum


class HTTPError(enum.IntEnum):
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


class APPException(Exception):
    """
    This Exception is use to raise exception from the business logic
    """

    def __init__(self, error: enum.IntEnum):
        self.code = error.value
        self.message = error.name


class HTTPException(Exception):
    """
    This Exception is use to raise exception to the http level
    """

    def __init__(self, error: HTTPError):
        self.code = error.value
        self.message = error.name
