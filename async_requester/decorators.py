import asyncio
import sys
from functools import wraps

from async_requester.utils import info

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def connection_retry(func):
    '''A simple decorator 
    handle errors that may appear due to the abundance of requests or incorrect data
    If error appear -> tries to retry request 5 times with 2 seconds delay
    '''
    @wraps(func)
    async def wrap(*args, **kwargs):
        retries = 1
        while retries < 6:
            try:
                result = await func(*args, **kwargs)
            except Exception as ex:
                info(f'Got unexpected error {ex}\n'
                    f'Retrying to connect...{retries}')
                retries += 1
                await asyncio.sleep(2)
            else:
                return result
        raise Exception('Maximum connections retries exceeded')
    return wrap
