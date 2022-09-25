import asyncio
import sys
from typing import Any, Awaitable, Callable, TypeVar, cast
from functools import wraps, partial
import warnings

from .logging import info

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

T = TypeVar("T", bound=Callable[..., Any])


def decohints(decorator: Callable) -> Callable:
    return decorator


def connection_retry(func):
    '''A simple decorator 
    handle errors that may appear due to the abundance of requests or incorrect data
    If error appear -> tries to retry request 5 times with 2 seconds delay
    '''
    @wraps(func)
    async def wrap(*args, **kwargs):
        retries = 1
        err = None
        while retries < 6:
            try:
                result = await func(*args, **kwargs)
            except Exception as ex:
                info(f'Got unexpected error {ex}\n'
                    f'Retrying to connect...{retries}')
                retries += 1
                await asyncio.sleep(2)
                err = ex
            else:
                return result
            
        raise Exception(f'Maximum connections retries exceeded\n{err}')
    return wrap


def async_test(coro):
    """
    Simple decorator to run async tests with unittest. Ignoring ResourceWarning
    """
    @wraps(coro)
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(coro(*args, **kwargs))
            finally:
                loop.close()
    return wrapper

@decohints
def sync_to_async(func: T):
    @wraps(func)
    async def run_in_executor(*args, **kwargs):
        loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(None, pfunc)

    return cast(Awaitable[T], run_in_executor)


@decohints
def sync_to_async_class(_class: Callable) -> Callable:
    class Executor:
        __attr = None 

        def __init__(self, *args, **kwargs):
            self._object = _class(*args, **kwargs)
        
        @wraps(__attr)
        async def _run_in_executor(self, *args, **kwargs):
            loop = asyncio.get_event_loop()
            pfunc = partial(self.__attr, *args, **kwargs)
            return await loop.run_in_executor(None, pfunc)
    
    
        def __getattribute__(self, __name: str) -> Any | Awaitable[Callable]:
            try:
                self_attr = super().__getattribute__(__name)
            except AttributeError:
                pass 
            else:
                return self_attr 
            
            self.__attr = self._object.__getattribute__(__name)
            if isinstance(self.__attr, type(self.__init__)):
                return cast(Awaitable[Callable], self._run_in_executor)
            
            return self.__attr 
    return Executor