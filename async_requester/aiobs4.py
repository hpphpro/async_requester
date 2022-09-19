import bs4 
from bs4.element import (
    Tag, 
    ResultSet, 
    NavigableString,  
    SoupStrainer,
    PageElement
    
)

from functools import partial, wraps
from typing import (
    Any, 
    Awaitable, 
    Callable, 
    TypeVar, 
    cast, 
    TypeAlias, 
    Iterable, 
    Pattern,
)
import asyncio



_SimpleStrainable: TypeAlias = str | bool | None | bytes | Pattern[str] | Callable[[str], bool] | Callable[[Tag], bool]
_Strainable: TypeAlias = _SimpleStrainable | Iterable[_SimpleStrainable]

T = TypeVar("T", bound=Callable[..., Any])


def decohints(decorator: Callable) -> Callable:
    return decorator

@decohints
def sync_to_async(func: T):
    @wraps(func)
    async def run_in_executor(*args, **kwargs):
        loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(None, pfunc)

    return cast(Awaitable[T], run_in_executor)


class AsyncBeatifulSoup(bs4.BeautifulSoup):
    __slots__= ()
    
    @sync_to_async
    def aselect(
        self, 
        selector: str, 
        namespaces: Any | None = None, 
        limit: int | None = None, 
        **kwargs
        ) -> ResultSet[Tag]:
        return super().select(selector, namespaces, limit, **kwargs)
    
    @sync_to_async
    def aselect_one(
        self, 
        selector: str, 
        namespaces: Any | None = None, 
        **kwargs
        ) -> Tag | None:
        return super().select_one(selector, namespaces, **kwargs)
    
    @sync_to_async
    def afind(
        self, 
        name: _Strainable | None = None, 
        attrs: dict[str, _Strainable] | _Strainable = {}, 
        recursive: bool = True, 
        string: _Strainable | None = None, 
        **kwargs: _Strainable
        ) -> Tag | NavigableString | None:
        return super().find(name, attrs, recursive, string, **kwargs)
    
    @sync_to_async
    def afind_all(
        self, 
        name: _Strainable | None = None, 
        attrs: dict[str, _Strainable] | _Strainable = {}, 
        recursive: bool = None, string: _Strainable | None = True, 
        limit: int | None = None, 
        **kwargs: _Strainable
        ) -> ResultSet[Any]:
        return super().find_all(name, attrs, recursive, string, limit, **kwargs)
    
    @sync_to_async
    def afind_all_next(
        self, name: _Strainable | SoupStrainer | None = None, 
        attrs: dict[str, _Strainable] | _Strainable = {}, 
        string: _Strainable | None = None, limit: int | None = None, 
        **kwargs: _Strainable
        ) -> ResultSet[PageElement]:
        return super().find_all_next(name, attrs, string, limit, **kwargs)
    
    @sync_to_async
    def afind_all_previous(
        self, name: _Strainable | SoupStrainer | None = None, 
        attrs: dict[str, _Strainable] | _Strainable = {}, 
        string: _Strainable | None = None, 
        limit: int | None = None, 
        **kwargs: _Strainable
        ) -> ResultSet[PageElement]:
        return super().find_all_previous(name, attrs, string, limit, **kwargs)
    
    @sync_to_async
    def afind_next_sibling(
        self, 
        name: _Strainable | SoupStrainer | None = None, 
        attrs: dict[str, _Strainable] | _Strainable = {}, 
        string: _Strainable | None = None, 
        **kwargs: _Strainable
        ) -> Tag | NavigableString | None:
        return super().find_next_sibling(name, attrs, string, **kwargs)
    
    @sync_to_async
    def afind_next(
        self, 
        name: _Strainable | SoupStrainer | None = None, 
        attrs: dict[str, _Strainable] | _Strainable = {}, 
        string: _Strainable | None = None, 
        **kwargs: _Strainable
        ) -> Tag | NavigableString | None:
        return super().find_next(name, attrs, string, **kwargs)
    
    @sync_to_async
    def afind_next_siblings(
        self, 
        name: _Strainable | SoupStrainer | None = None, 
        attrs: dict[str, _Strainable] | _Strainable = {}, 
        string: _Strainable | None = None, limit: int | None = None, 
        **kwargs: _Strainable
        ) -> ResultSet[PageElement]:
        return super().find_next_siblings(name, attrs, string, limit, **kwargs)
    
    @sync_to_async
    def afind_parents(
        self, 
        name: _Strainable | SoupStrainer | None = None, 
        attrs: dict[str, _Strainable] | _Strainable = {}, 
        limit: int | None = None, 
        **kwargs: _Strainable
        ) -> ResultSet[Tag]:
        return super().find_parents(name, attrs, limit, **kwargs)
    
    @sync_to_async
    def afind_previous(
        self, 
        name: _Strainable | SoupStrainer | None = None, 
        attrs: dict[str, _Strainable] | _Strainable = {}, 
        string: _Strainable | None = None, 
        **kwargs: _Strainable
        ) -> Tag | NavigableString | None:
        return super().find_previous(name, attrs, string, **kwargs)
    
    @sync_to_async
    def afind_previous_sibling(
        self, 
        name: _Strainable | SoupStrainer | None = None, 
        attrs: dict[str, _Strainable] | _Strainable = {}, 
        string: _Strainable | None = None, 
        **kwargs: _Strainable
        ) -> Tag | NavigableString | None:
        return super().find_previous_sibling(name, attrs, string, **kwargs)
    
    @sync_to_async
    def afind_previous_siblings(
        self, 
        name: _Strainable | SoupStrainer | None = None, 
        attrs: dict[str, _Strainable] | _Strainable = {}, 
        string: _Strainable | None = None, 
        limit: int | None = None, 
        **kwargs: _Strainable
        ) -> ResultSet[PageElement]:
        return super().find_previous_siblings(name, attrs, string, limit, **kwargs)
    