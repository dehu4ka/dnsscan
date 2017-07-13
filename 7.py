import signal
import curio
import dns.query
from file_functions import get_ips_list_from_file
from dnscheck import check_reply

MAX_THREADS = 100


async def is_resolver_working(test_ip):
    print('Checking working resolver: ', test_ip)
    answer = check_reply(test_ip)
    if answer:
        print(test_ip + ' is open resolver')
        return True
    # print(test_ip + ' is NOT an open resolver')
    return False

async def launcher():
    ip_list = get_ips_list_from_file('1.out')
    chunks = [ip_list[MAX_THREADS * i:MAX_THREADS * (i + 1)] for i in range(int(len(ip_list) / MAX_THREADS) + 1)]

    ip = chunks[0][0]
    async with curio.TaskGroup() as f:
        for ip in chunks[0]:
            # print('spawning IP: ', ip)
            f.spawn(is_resolver_working, ip)
            f.spawn(is_resolver_working, ip)
        try:
            await curio.sleep(20)
        except curio.CancelledError:
            raise

async def parent():
    launcher_task = curio.spawn(launcher)
    launcher_task.join()







if __name__ == '__main__':
    curio.run(parent)
