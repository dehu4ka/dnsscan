import asyncio
import time

async def my_task(seconds):
    """
    A task to do for a number of seconds
    """
    print('This task is taking {} seconds to complete'.format(
        seconds))
    time.sleep(seconds)
    return 'task finished'


if __name__ == '__main__':
    my_event_loop = asyncio.get_event_loop()
    try:
        print('task creation started')
        task_obj1 = my_event_loop.create_task(my_task(seconds=1))
        task_obj2 = my_event_loop.create_task(my_task(seconds=2))
        task_obj3 = my_event_loop.create_task(my_task(seconds=3))
        my_event_loop.run_until_complete(task_obj1)
        my_event_loop.run_until_complete(task_obj2)
        my_event_loop.run_until_complete(task_obj3)
    finally:
        my_event_loop.close()

    print("The task's result was: {}".format(task_obj1.result()))
    print("The task's result was: {}".format(task_obj2.result()))
    print("The task's result was: {}".format(task_obj3.result()))