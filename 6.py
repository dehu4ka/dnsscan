import curio

start_evt = curio.Event()

async def countdown(n):
    while n > 0:
        print('T-minus', n)
        await curio.sleep(1)
        n -= 1

async def friend(name):
    print('Hi, my name is', name)
    print('Playing Minecraft')
    try:
        await curio.sleep(1000)
    except curio.CancelledError:
        print(name, 'going home')
        raise

async def kid():
    while True:
        try:
            print('Can I play?')
            await curio.timeout_after(1, start_evt.wait)
            break
        except curio.TaskTimeout:
            print('Wha!?!')

    print('Building the Millenium Falcon in Minecraft')
    async with curio.TaskGroup() as f:
        await f.spawn(friend, 'Max')
        await f.spawn(friend, 'Lillian')
        await f.spawn(friend, 'Thomas')
        try:
            await curio.sleep(1000)
        except curio.CancelledError:
            print('Fine. Saving my work.')
            raise

async def parent():
    kid_task = await curio.spawn(kid)
    await curio.sleep(5)

    print('Yes, go play')
    await start_evt.set()
    await curio.sleep(5)

    print("Let's go")
    count_task = await curio.spawn(countdown, 10)
    await count_task.join()

    print("We're leaving!")
    try:
        await curio.timeout_after(10, kid_task.join)
    except curio.TaskTimeout:
        print('I warned you!')
        await kid_task.cancel()
    print('Leaving!')

if __name__ == '__main__':
    curio.run(parent)