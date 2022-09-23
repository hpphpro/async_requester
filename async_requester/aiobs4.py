import bs4 

from functools import partial, wraps
from typing import (
    Any, 
    Awaitable, 
    Callable, 
    TypeVar, 
    cast, 
)
import asyncio



T = TypeVar("T", bound=Callable[..., Any])


def decohints(decorator: Callable) -> Callable:
    return decorator


@decohints
def sync_to_async(_class: T) -> Callable:
    class Executor:
        __attr = None 

        def __init__(self, *args, **kwargs):
            self._object = _class(*args, **kwargs)
        
        @wraps(__attr)
        async def _run_in_executor(self, *args, **kwargs):
            loop = asyncio.get_event_loop()
            pfunc = partial(self.__attr, *args, **kwargs)
            return await loop.run_in_executor(None, pfunc)
    
    
        def __getattribute__(self, __name: str) -> Any | Awaitable[T]:
            try:
                self_attr = super().__getattribute__(__name)
            except AttributeError:
                pass 
            else:
                return self_attr 
            
            self.__attr = self._object.__getattribute__(__name)
            if isinstance(self.__attr, type(self.__init__)):
                return cast(Awaitable[T], self._run_in_executor)
            
            return self.__attr 
    return Executor

@sync_to_async
class AsyncBeatifulSoup(bs4.BeautifulSoup):
    __slots__ = ()

