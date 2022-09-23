import logging
from logging import Logger

from random import choice
from .aiobs4 import AsyncBeatifulSoup
  
  
def get_random_useragent() -> str:
    """Getting random useragent at start"""
    user_agents_list = (
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    )  
    
    return choice(user_agents_list)


class Response:
    
    def __init__(
        self, 
        request_url: str , 
        response_url: str, 
        headers: dict, 
        cookies: dict, 
        status_code: int, 
        content: bytes | dict | None = None
        ) -> None:
        self.request_url = request_url
        self.response_url = response_url
        self.headers = headers
        self.cookies = cookies
        self.status_code = status_code
        self.content = content
    
    @property
    def html(self) -> AsyncBeatifulSoup:
        parser = 'lxml'
        if isinstance(self.content, (bytes, str)):
            return AsyncBeatifulSoup(markup=self.content, features=parser)
        
        raise TypeError(f'Expected bytes or string, got {type(self.content)}')
    
    
    
def info(message: str) -> Logger:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        level=logging.INFO
    )
    logger = logging.getLogger()
    return logger.info(message)