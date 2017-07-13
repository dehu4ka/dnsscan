import asyncio
from random import randint

async def do_stuff(ip, port):
    print('About to open a connection to {ip}'.format(ip=ip))
    reader, writer = await asyncio.open_connection(ip, port)

    print('Connection open to {ip}'.format(ip=ip))
    await asyncio.sleep(randint(0, 5))

    writer.close()
    print('Closed connection to {ip}'.format(ip=ip))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    work = [
        asyncio.ensure_future(do_stuff('8.8.8.8', '53')),
        asyncio.ensure_future(do_stuff('8.8.4.4', '53')),
    ]

    loop.run_until_complete(asyncio.gather(*work))