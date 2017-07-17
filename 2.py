import asyncio
import functools
import signal
import time
import aioredis
from async_dns import types
from async_dns.resolver import ProxyResolver

from file_functions import get_ips_list_from_file

# magic var
MAX_THREADS = 1000

async def is_resolver_working(test_ip):
    # loop = asyncio.get_event_loop()
    resolver = ProxyResolver()
    resolver.set_proxies([test_ip, ])
    # res = loop.run_until_complete(resolver.query('www.baidu.com', types.A))

    res = await resolver.query('www.google.com', types.A)
    # print('scanning: %s' % test_ip)
    # print(res)
    if res and len(res.an) > 0:  # response is exists and have A-records in it
        # print(test_ip + ' is open resolver')
        # print(res)

        # this is works, 5000 thread size processed in 10 seconds. without redis - 5 seconds, delta is 5 seconds,
        # so it will be 0.1 sec to async redis call
        redis = await aioredis.create_redis(('localhost', 6379))
        await redis.rpush('resolvers', test_ip)
        redis.close()
        return True
    # print(test_ip + ' is NOT an open resolver')
    return False


if __name__ == '__main__':
    total_start_time = time.time()
    ip_list = get_ips_list_from_file('2.out')

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
        print('Time for %s records is: %s' % (len(p), str(end_time - start_time)))

    total_end_time = time.time()
    print('TOTAL time for %s records is: %s' % (len(ip_list), str(total_end_time - total_start_time)))
    print('done')
