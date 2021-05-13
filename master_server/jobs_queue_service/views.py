import asyncio

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse

from .util.aredis_queue import NLUQueue
import uuid

def index(request):
    return HttpResponse("Hello, world. You're at the jobs_queue_service index.")


def json(request: WSGIRequest):
    post_data = dict(request.POST)
    get_data = dict(request.GET)
    request_method = str(request.method)
    request_header = str(request.META)


    return JsonResponse({
        "post_data": post_data,
        "get_data": get_data,
        "request_method": request_method,
        "request_header": request_header,
    })


def hello_world(request):
    return render(request, 'hello_world.html', {
        'current_time': str(datetime.now()),
    })


async def worker_test(request):
    redis_to_MDL = NLUQueue(name="MDL", namespace="common")
    redis_to_API = NLUQueue(name="API", namespace="common")

    async def __new_work__(item):
        request_id = str(uuid.uuid4())
        print(f"new_work: {item}")
        await redis_to_MDL.enqueue({
            "obj": item,
            "request_id": request_id
        })
        return request_id

    async def __get_responds__(request_id: str):
        res = await redis_to_API.get_msg_by_direct_id(request_id)
        print(f"get_responds: {res}")
        return res

    if str(request.method) == "GET":
        get_data = dict(request.GET)
        request_id = await __new_work__(get_data)
        worker_response = await __get_responds__(request_id)
        time = 0
        while worker_response is None and time < 500:
            worker_response = await __get_responds__(request_id)
            time += 1
            await asyncio.sleep(0.1)
        else:
            return JsonResponse({
                'foo': get_data,
                "worker_response": str(worker_response)
            })
    else:
        return HttpResponse("Only support GET method")