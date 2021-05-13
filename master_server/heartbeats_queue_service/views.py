import asyncio

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse

from .util.aredis_queue import NLUQueue
import uuid



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


heartbeats_log = []


async def index(request):
    redis_to_API = NLUQueue(name="API", namespace="common")

    async def __get_heartbeats__():
        res = await redis_to_API.dequeue_nowait()
        print(f"get_responds: {res}")
        return res

    if str(request.method) == "GET":
        global heartbeats_log
        heartbeats = await __get_heartbeats__()
        while heartbeats is not None:
            heartbeats_log.append(heartbeats)
            heartbeats = await __get_heartbeats__()
        else:
            heartbeats_log = heartbeats_log[-100:]
            return JsonResponse({
                "heartbeats_log": heartbeats_log
            })
    else:
        return HttpResponse("Only support GET method")