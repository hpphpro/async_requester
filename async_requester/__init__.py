from aiohttp import ClientSession

import asyncio, sys
from typing import AsyncGenerator, Any, NoReturn

from async_requester.decorators import connection_retry
from async_requester.metaclasses import Singleton
from async_requester.utils import Response, get_random_useragent


__all__ = [
    'get_random_useragent',
    'get_latest_useragent',
    'AsyncRequest'
]


class AsyncRequest(metaclass=Singleton):
    """
    A Singleton class that makes async request and getting data from url/urls
    <options> contents simple request options:
        auth,
        json,
        data,
        params,
        allow_redirects,
        cookies,
        headers,
        ...
    step variable indicates how many requests in a row do you want to do.
    NOTE:
        - Do not try to use 1000/2000/etc step value (but it may work)
        remember, we should be nice to the server
        Usage:
            AsyncRequest().get('https://google.com') -> to get single site data
            AsyncRequest().post('https://google.com') -> post request
            ...
            AsyncRequest().collect_data(['https://google.com', 'https://youtube.com']) -> to get a list with sites data
    """
    def __init__(self, step: int = 10) -> None:
        self.step = step 
        self.headers: dict = {
            'user-agent': get_random_useragent(),
        }
        self.__session: ClientSession = self.create_session()
        
    async def create_session(self) -> ClientSession:
        '''Making session'''
        async with ClientSession(headers=self.headers) as session:
            while True:
                yield session
                
                
    async def get(self, url: str, as_json: bool = False, **options) -> Response | NoReturn:
        return await self._fetch(url=url, method='get', as_json=as_json, **options)
    
    
    async def post(self, url: str, as_json: bool = False, **options) -> Response | NoReturn:
        return await self._fetch(url=url, method='post', as_json=as_json, **options)
    
    
    async def patch(self, url: str, as_json: bool = False, **options) -> Response | NoReturn:
        return await self._fetch(url=url, method='patch', as_json=as_json, **options)
    
    
    async def options(self, url: str, as_json: bool = False, **options) -> Response | NoReturn:
        return await self._fetch(url=url, method='options', as_json=as_json, **options)
    
    
    async def put(self, url: str, as_json: bool = False, **options) -> Response | NoReturn:
        return await self._fetch(url=url, method='put', as_json=as_json, **options)
    
    @connection_retry
    async def _fetch(
        self, 
        url: str, 
        method: str, 
        as_json: bool = False, 
        **options
        ) -> Response | NoReturn:
        """
        Args:
            url (str): a url that data you want get from
            method (str, optional): request method. 
            as_json (bool, optional): equal to .json() from basic request. Defaults to False.

        Raises:
            AttributeError: Supports only get/post/put/patch/options methods

        Returns:
            Response: a data from request
        """
        session = await anext(self.__session) # getting current session
        request = {
            'post': session.post,
            'get': session.get,
            'put': session.put,
            'options': session.options,
            'patch': session.patch,
        }
        
        if method not in request:
            raise AttributeError(f'Expected request method, got {method}')
        if not options.get('headers'):
            options['headers'] = self.headers
    
        async with request[method](url=url, **options) as response:
            if response.status == 200:
                return Response(
                    content=await response.read() if not as_json else await response.json(),
                    request_url=url,
                    response_url=response.url,
                    headers=response.headers,
                    cookies=response.cookies,
                    status_code=response.status
                )
            return Response(
                    request_url=url,
                    response_url=response.url,
                    headers=response.headers,
                    cookies=response.cookies,
                    status_code=response.status
                )
    
    async def _collect_tasks(
        self, 
        urls: list | tuple, 
        method: str, 
        as_json: bool = False, 
        **options
        ) -> AsyncGenerator[list[Response], Any]:
        """

        Args:
            urls (list | tuple): a urls that data you want to get from
            method (str, optional): same to ._fetch() method
            as_json (bool, optional): same to ._fetch() method

        Yields:
            Iterator[list[Response]]: returns an AsyncGenerator with list of responses inside
        """
        if not isinstance(urls, (tuple, list)):
            urls = tuple(urls)
        step = self.step if len(urls) >= self.step else len(urls)
        tasks = set()
        for index in range(0, len(urls), step):
            for url in urls[index:index+step]:
                tasks.add(asyncio.create_task(self._fetch(url, method=method, as_json=as_json, **options)))
            yield await asyncio.gather(*tasks)
            tasks.clear()
            
    async def collect_data(
        self, 
        urls: list | tuple, 
        method: str = 'get', 
        as_json: bool = False, 
        **options
        ) -> AsyncGenerator[list[Response], Any]:
        return self._collect_tasks(urls, method=method, as_json=as_json, **options)
    
    
async def get_latest_useragent() -> str | None:
    """
    Returns:
        str | None: Trying to get the latest useragent for your browser
        
    It's can be useful if site has cloudflare and checks your platform with useragent
    and compare it. But it may be not enough, check on cookies as well.
    """
    
    linux_ua = 'Mozilla/5.0 (X11; Linux x86_64)'
    windows_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    session = AsyncRequest()
    response = await session.get('https://www.whatismybrowser.com/guides/the-latest-user-agent/windows')
    data = await response.html.select('table > tbody > tr')
    new_ua = None
    for col in data:
        chrome = col.select_one('td > b')
        if chrome and chrome.get_text(strip=True).lower() == 'chrome':
            ua = col.select_one('span.code')
            if ua:
                new_ua = ua.get_text(strip=True)
                break
    if new_ua:
        new_data = new_ua.split(')', 1)[-1]
        
        match sys.platform:
            case 'win32':
                new_ua = f'{windows_ua}{new_data}'
            case 'linux' | 'linux2':
                new_ua = f'{linux_ua}{new_data}'
            case _:
                raise Exception(f'This function expected Linux or Windows platform, not {sys.platform}')
        
    return new_ua
    