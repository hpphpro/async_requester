from ..aiobs4 import AsyncBeatifulSoup

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