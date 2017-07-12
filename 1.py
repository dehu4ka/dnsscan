import dns.resolver


def check_reply(host=None):
    if not host:
        return False
    resolver = dns.resolver.Resolver()
    resolver.nameservers = host
    answer = resolver.query('google.com', 'A')
    print(answer)





if __name__ == '__main__':
    check_reply('88.205.225.242')
