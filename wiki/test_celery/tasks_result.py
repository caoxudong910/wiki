# 生成 worker 消费者
from celery import Celery


# 初始化celery对象
app = Celery('caoxudong',broker='redis://:@127.0.0.1:6379/1',
             backend='redis://:@127.0.0.1:6379/2')

# 创建具体执行的内容
@app.task()
def test_task_result(a,b):
    print('-----is run ing-----')
    return a+b

# celery -A tasks_result worker --loglevel=info