# 生成 worker 消费者
from celery import Celery


# 初始化celery对象
app = Celery('caoxudong',broker='redis://:@127.0.0.1:6379/1')

# 创建
@app.task()
def test_task():
    print('-----is run ing-----')

# celery -A tasks worker --loglevel=info