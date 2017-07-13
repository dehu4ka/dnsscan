import gevent
from gevent import socket
from gevent.pool import Pool
from file_functions import check_reply, get_ips_list_from_file

N = 1000
pool = Pool(10)
finished = 0


def job(url):
    global finished
    try:
        try:
            ip = socket.gethostbyname(url)
            print('%s = %s' % (url, ip))
        except socket.gaierror as ex:
            print('%s failed with %s' % (url, ex))
    finally:
        finished += 1


ip_list = get_ips_list_from_file('1.out')


with gevent.Timeout(2, False):
    for ip in ip_list:
        pool.spawn(check_reply, ip)
    pool.join()


