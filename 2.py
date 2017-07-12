import asyncio
from async_dns import types
from async_dns.resolver import ProxyResolver

from file_functions import get_ips_list_from_file


"""
loop = asyncio.get_event_loop()
resolver = ProxyResolver()
resolver.set_proxies(['88.205.225.243', ])
res = loop.run_until_complete(resolver.query('www.baidu.com', types.A))
print(res)
"""

async def is_resolver_working(test_ip):
    # loop = asyncio.get_event_loop()
    resolver = ProxyResolver()
    resolver.set_proxies([test_ip, ])
    # res = loop.run_until_complete(resolver.query('www.baidu.com', types.A))
    res = await resolver.query('www.baidu.com', types.A)
    if res:
        print(test_ip + ' is open resolver')
        return True
    print(test_ip + ' is NOT an open resolver')
    return False

if __name__ == '__main__':
    ip_list = get_ips_list_from_file('1.out')

    event_loop = asyncio.get_event_loop()
    try:
        for ip in ip_list:
            print('start checking ' + ip)
            task = event_loop.run_until_complete(is_resolver_working(ip))
    finally:
        event_loop.close()
