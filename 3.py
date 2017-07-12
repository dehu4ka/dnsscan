import asyncio
from async_dns import types
from async_dns.resolver import ProxyResolver

"""loop = asyncio.get_event_loop()
resolver = ProxyResolver()
res = loop.run_until_complete(resolver.query('www.baidu.com', types.A))
print(res)"""


resolver = ProxyResolver()
res = resolver.query('www.baidu.com', types.A)
print(res)