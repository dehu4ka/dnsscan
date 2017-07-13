from dns.resolver import Resolver
import dns.exception


def check_reply(host=None, timeout=2.0):
    if not host:
        return False
    resolver = Resolver()
    resolver.nameservers = [host, ]
    resolver.timeout = timeout
    resolver.lifetime = timeout
    try:
        answer = resolver.query('google.com')
    except dns.exception.Timeout:
        print(host, ":Timeout")
        return False
    except dns.resolver.NoNameservers:
        print(host, ":No open resolver")
        return False
    return True


def get_ips_list_from_file(filename):
    ip_list = list()
    counter = 0
    with open(filename) as f:
        for line in f:
            line = f.readline().replace("\n", "")
            ip_list.append(line)
            counter += 1
            if counter > 100000:
                break
    return ip_list

if __name__ == '__main__':
    ip_list = get_ips_list_from_file('1.out')
    print(ip_list)
