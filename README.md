# async_requester: Asynchronous requests template
A template for async request<br>
Made to simplify async requests. Supports single requests and multiply<br>
Basic Usage:<br>
```python
from async_requester import AsyncRequest 
import asyncio


async def get_google_page():
    arequests = AsyncRequest(step=100) # step variable means how many request will be in a row
    data = await arequests.collect_data(['https://google.com' for _ in range(100)]) # default usage with 'get' request method
    # data = await arequests.collect_data(['https://google.com' for _ in range(100)], method='post') or the same with post or any
    async for pages_list in data: # data variable is an async_generator
        for page in pages_list:
            response_content = page.content
            response_status = page.status_code
            response_headers = page.headers
            ...
    get_request_response = await arequests.get(url='https://google.com')
    page_data = get_request_response.content
    # you can make the same with 'post' or any other request method
    post_request_response = await arequests.post(url='https://google.com', json='myjson')
    put_request_response = await arequests.put(url='https://google.com', data='mydata')
    ...
asyncio.run(get_google_page())
```
`async_requester` was made with aiohttp module
