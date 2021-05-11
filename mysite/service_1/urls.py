from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hello', views.hello_world, name='hello'),
    path('json', views.json, name='json'),
    path('worker', views.worker_test, name='worker_test'),

]