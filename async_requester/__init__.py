from aiohttp import ClientSession

import asyncio
from typing import AsyncGenerator, Any, NoReturn

from async_requester.decorators import connection_retry
from async_requester.metaclasses import Singleton
from async_requester.utils import Response, get_useragent





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
            'user-agent': get_useragent(),
        }
        self.__session: ClientSession = self.create_session()
        
    async def create_session(self) -> ClientSession:
        '''Making session'''
        async with ClientSession(headers=self.headers) as session:
            while True:
                yield session
                
                
    async def get(self, url: str, json_data: bool = False, **options) -> Response | NoReturn:
        return await self._fetch(url=url, method='get', json_data=json_data, **options)
    
    
    async def post(self, url: str, json_data: bool = False, **options) -> Response | NoReturn:
        return await self._fetch(url=url, method='post', json_data=json_data, **options)
    
    
    async def patch(self, url: str, json_data: bool = False, **options) -> Response | NoReturn:
        return await self._fetch(url=url, method='patch', json_data=json_data, **options)
    
    
    async def options(self, url: str, json_data: bool = False, **options) -> Response | NoReturn:
        return await self._fetch(url=url, method='options', json_data=json_data, **options)
    
    
    async def put(self, url: str, json_data: bool = False, **options) -> Response | NoReturn:
        return await self._fetch(url=url, method='put', json_data=json_data, **options)
    
    @connection_retry
    async def _fetch(
        self, 
        url: str, 
        method: str, 
        json_data: bool = False, 
        **options
        ) -> Response | NoReturn:
        """
        Args:
            url (str): a url that data you want get from
            method (str, optional): request method. 
            json_data (bool, optional): equal to .json() from basic request. Defaults to False.

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
                    content=await response.read() if not json_data else await response.json(),
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
        json_data: bool = False, 
        **options
        ) -> AsyncGenerator[list[Response], Any]:
        """

        Args:
            urls (list | tuple): a urls that data you want to get from
            method (str, optional): same to ._fetch() method
            json_data (bool, optional): same to ._fetch() method

        Yields:
            Iterator[list[Response]]: returns an AsyncGenerator with list of responses inside
        """
        if not isinstance(urls, (tuple, list)):
            urls = tuple(urls)
        step = self.step if len(urls) >= self.step else len(urls)
        tasks = set()
        for index in range(0, len(urls), step):
            for url in urls[index:index+step]:
                tasks.add(asyncio.create_task(self._fetch(url, method=method, json_data=json_data, **options)))
            yield await asyncio.gather(*tasks)
            tasks.clear()
            
    async def collect_data(
        self, 
        urls: list | tuple, 
        method: str = 'get', 
        json_data: bool = False, 
        **options
        ) -> AsyncGenerator[list[Response], Any]:
        return self._collect_tasks(urls, method=method, json_data=json_data, **options)
    