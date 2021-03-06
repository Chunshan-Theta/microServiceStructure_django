import json
import datetime
from util.aredis_queue import NLUQueue
import asyncio

redis_to_MDL = NLUQueue(name="MDL", namespace="common")
redis_to_API = NLUQueue(name="API", namespace="common")


async def get_work():
    res = await redis_to_MDL.dequeue_nowait()
    print(f"get_work: {res}")
    res = json.loads(res.replace("'", "\"")) if res is not None else None
    return res


async def send_responds(obj,request_id):
    print(f"send_responds: {obj}")
    return await redis_to_API.set_msg_by_direct_id_ex(id=request_id, second2expire=300, value=obj)


async def send_heartbeats():
    return await redis_to_API.enqueue({"status": True, "label": "sample worker", "datetime":str(datetime.datetime.now())})


async def main():
    idx = 0
    while True:
        task = await get_work()
        if task is not None:
            obj = task.get("obj", None)
            request_id = task.get("request_id", None)
            await send_responds(obj, request_id)
        else:
            idx += 1
            if idx == 30:
                await send_heartbeats()
                idx = 0
            await asyncio.sleep(1)


asyncio.run(main())