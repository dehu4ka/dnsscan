import asyncio
import functools
import signal
import time
from async_dns import types
from async_dns.resolver import ProxyResolver

from file_functions import get_ips_list_from_file

MAX_THREADS = 10000

async def is_resolver_working(test_ip):
    # loop = asyncio.get_event_loop()
    resolver = ProxyResolver()
    resolver.set_proxies([test_ip, ])
    # res = loop.run_until_complete(resolver.query('www.baidu.com', types.A))
    res = await resolver.query('www.baidu.com', types.A)
    if res:
        # print(test_ip + ' is open resolver')
        # print(res)
        return True
    # print(test_ip + ' is NOT an open resolver')
    return False


if __name__ == '__main__':
    ip_list = get_ips_list_from_file('1.out')

    event_loop = asyncio.get_event_loop()


    def ask_exit(signame):
        print("got signal %s: exit" % signame)
        event_loop.stop()

    for signame in ('SIGINT', 'SIGTERM'):
        event_loop.add_signal_handler(getattr(signal, signame), functools.partial(ask_exit, signame))

    """for ip in ip_list:
        # print('start checking ' + ip)
        # task = event_loop.run_until_complete(is_resolver_working(ip))
        asyncio.ensure_future(is_resolver_working(ip))"""

    # ip_list[MAX_THREADS*i:MAX_THREADS*(i+1)]
    chunks = [ip_list[MAX_THREADS*i:MAX_THREADS*(i+1)] for i in range(int(len(ip_list)/MAX_THREADS) + 1)]

    work = list()
    counter = 0
    for p in chunks:
        start_time = time.time()
        for ip in p:
            work.append(asyncio.ensure_future(is_resolver_working(ip)))
        event_loop.run_until_complete(asyncio.gather(*work))
        end_time = time.time()
        print('Time: ' + str(end_time - start_time))
    print('done')
