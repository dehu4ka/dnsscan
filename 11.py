import asyncio
import functools
import signal
import time
import aioredis
from async_dns import types
from async_dns.resolver import ProxyResolver
import sys
import fileinput
import redis

from file_functions import get_ips_list_from_file

# magic var
MAX_THREADS = 2000

async def is_resolver_working(test_ip):
    # loop = asyncio.get_event_loop()
    try:
        resolver = ProxyResolver()
        resolver.set_proxies([test_ip, ])
        # res = loop.run_until_complete(resolver.query('www.baidu.com', types.A))
        res = await resolver.query('abc.com', types.ANY, timeout=1.5)
        # print('scanning: %s' % test_ip)
        # print(res)
        if res and len(res.an) > 5:  # response is exists and have A-records in it
            # print(test_ip + ' is open resolver')
            # print(len(res.an))
            # print(res)

            # this is works, 5000 thread size processed in 10 seconds. without redis - 5 seconds, delta is 5 seconds,
            # so it will be 0.1 sec to async redis call
            redis = await aioredis.create_redis(('localhost', 6379))
            await redis.rpush('resolvers', test_ip)
            redis.close()
            return True
    except TypeError:
        return False
    # print(test_ip + ' is NOT an open resolver')
    return False

if __name__ == '__main__':
    total_start_time = time.time()
    redis_db = redis.StrictRedis()

    event_loop = asyncio.get_event_loop()

    def ask_exit(signame):
        print("got signal %s: exit" % signame)
        event_loop.stop()
        sys.exit(1)

    for signame in ('SIGINT', 'SIGTERM'):
        event_loop.add_signal_handler(getattr(signal, signame), functools.partial(ask_exit, signame))

    counter = 0
    work = list()
    with fileinput.input(files=('2.out',)) as f:
        for line in f:
            work.append(asyncio.ensure_future(is_resolver_working(line.strip())))
            counter += 1
            if counter % MAX_THREADS == 0:
                start_time = time.time()
                event_loop.run_until_complete(asyncio.gather(*work))
                work[:] = []  # deletes all elements in work list
                found_resolvers = redis_db.llen('resolvers')
                end_time = time.time()
                print('Time for %s records is: %s. %s open resolvers is found for now. Total %s IPs checked' %
                      (MAX_THREADS, str(end_time - start_time), found_resolvers, counter))

                # break
            """if counter > 100000:
                break"""
    total_end_time = time.time()
    print('TOTAL time for %s records is: %s' % (str(counter), str(total_end_time - total_start_time)))
    print('done')
