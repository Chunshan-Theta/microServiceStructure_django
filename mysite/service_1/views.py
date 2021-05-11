from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse
from .util.aredis_queue import NLUQueue


def index(request):
    return HttpResponse("Hello, world. You're at the service_1 index.")


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


redis_to_MDL = NLUQueue(name="MDL", namespace="common")
redis_to_API = NLUQueue(name="API", namespace="common")


async def worker_test(request):
    async def __new_work__(item):
        print(f"new_work: {item}")
        await redis_to_MDL.enqueue(item)

    async def __get_responds__():
        res = await redis_to_API.dequeue_nowait()
        print(f"get_responds: {res}")
        return res

    if str(request.method) == "GET":
        get_data = dict(request.GET)
        await __new_work__(get_data)
        return JsonResponse({'foo': get_data})
    else:
        return HttpResponse("Only support GET method")