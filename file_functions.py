from dns.resolver import Resolver
import dns.exception

"""
def get_ips_list_from_file(filename):
    ip_list = list()
    counter = 0
    with open(filename) as f:
        for line in f:
            line = f.readline().replace("\n", "")
            ip_list.append(line)
            counter += 1
            #if counter > 10000:
            #    break
    return ip_list


"""


def get_ips_list_from_file(filename):
    ip_list = list()
    counter = 0
    with open(filename) as f:
        lines = f.read().split("\n")
        for line in lines:
            ip_list.append(line)
            counter += 1
            #if counter > 10000:
            #    break
    return ip_list

if __name__ == '__main__':
    ip_list = get_ips_list_from_file('1.out')
    print(ip_list)
