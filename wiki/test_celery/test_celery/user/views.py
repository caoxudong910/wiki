import datetime
from .tasks import task_test
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def test_celery(request):
    # http://127.0.0.1:8000/user/test_celery
    # TODO 模拟worker将执行阻塞10秒任务
    task_test.delay()
    now = datetime.datetime.now()
    html = 'return at %s'%(now.strftime('%Y-%m-%d %H:%M:%S'))
    return HttpResponse(html)