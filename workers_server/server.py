from util.aredis_queue import NLUQueue
import asyncio

redis_to_MDL = NLUQueue(name="MDL", namespace="common")
redis_to_API = NLUQueue(name="API", namespace="common")


async def get_work():
    res = await redis_to_MDL.dequeue_nowait()
    print(f"get_work: {res}")
    return res


async def send_responds(item):
    print(f"send_responds: {item}")
    return await redis_to_API.enqueue(item)


async def main():
    while True:
        task = await get_work()
        if task is not None:
            new_text = "hello "+task
            await send_responds(new_text)
        else:
            await asyncio.sleep(1)


asyncio.run(main())