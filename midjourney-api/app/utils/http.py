import asyncio
from typing import Any, Callable, Coroutine, Dict, TypeVar, Union

from aiohttp import ClientError, ClientSession, hdrs
from app.utils.logger import setup_logger

T = TypeVar("T")

logger = setup_logger("http")


class MaxRetry:
    def __init__(self, max_retry: int = 0):
        self.max_retry = max_retry

    def __call__(
        self, connect_once: Callable[..., Coroutine[Any, Any, T]]
    ) -> Callable[..., Coroutine[Any, Any, T]]:
        async def connect_n_times(*args: Any, **kwargs: Any) -> T:
            retry = self.max_retry + 1
            while retry:
                try:
                    return await connect_once(*args, **kwargs)
                except ClientError as e:
                    await asyncio.sleep(1)
                    logger.warning(
                        f"request fail（{e.__class__.__name__}）, trying now，remaining {retry - 1}"
                    )
                except asyncio.TimeoutError:
                    logger.warning(
                        f"request timeout, trying now, remaining {retry - 1}"
                    )
                finally:
                    retry -= 1
            raise Exception("maximum number of retries exceeded")

        return connect_n_times


class FetchMethod:
    get = hdrs.METH_GET
    post = hdrs.METH_POST
    put = hdrs.METH_PUT


@MaxRetry(2)
async def fetch(
    session: ClientSession, url: str, method: str = FetchMethod.post, **kwargs
) -> Union[bool, None]:
    logger.debug(f"Fetch: {url}, {kwargs}")
    async with session.request(method, url, **kwargs) as resp:
        if not resp.ok:
            return None
        return True


@MaxRetry(2)
async def fetch_json(
    session: ClientSession, url: str, method: str = FetchMethod.post, **kwargs
) -> Union[Dict, None]:
    logger.debug(f"Fetch text: {url}")
    async with session.request(method, url, **kwargs) as resp:
        if not resp.ok:
            return None
        return await resp.json()
