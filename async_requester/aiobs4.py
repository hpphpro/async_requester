import bs4 
from .utils.decorators import sync_to_async_class


@sync_to_async_class
class AsyncBeatifulSoup(bs4.BeautifulSoup):
    __slots__ = ()

