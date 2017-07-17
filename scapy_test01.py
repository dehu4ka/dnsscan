from scapy.all import *


if __name__ == '__main__':
    a = IP(dst='88.205.232.5')/UDP(sport=RandShort(), dport=53)/DNS(rd=1, qd=DNSQR(qname="abc.com", qtype='ALL', qclass='IN'))
    # a.src = '212.220.33.20'
    print(ls(a))
    send(a)
