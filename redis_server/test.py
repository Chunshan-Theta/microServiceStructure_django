import asyncio
from aredis_queue import NLUQueue


async def main():
    redisserver = NLUQueue("test")
    s = await redisserver.qsize()
    print(f"redisserver: {s}")
    _ = await redisserver.enqueue({"a": 1})
    s = await redisserver.qsize()
    print(f"redisserver: {s}")

    while s > 0:
        r = await redisserver.dequeue_nowait()
        s = await redisserver.qsize()
        print(f"redisserver: {s},{r}")


asyncio.run(main())



