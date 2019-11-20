import datetime
import json
import time,hashlib

import jwt
from django.http import JsonResponse
from user.models import UserProfile


# Create your views here.
def make_token(username,login_time,exp):
    # 生成token
    key = 'cxd'
    now_time = time.time()
    payload = {'username':username,'login_time':str(login_time),'exp':int(now_time+exp)}
    return jwt.encode(payload,key,algorithm='HS256')


def tokens(request):
    # 验证用户
    if request.method != 'POST':
        result = {'code':20101,'error':'Please use POST !'}
        return JsonResponse(result)

    json_str = request.body
    if not json_str:
        result = {'code': 20102, 'error': 'Please give me data !'}
        return JsonResponse(result)
    json_obj = json.loads(json_str)
    username = json_obj.get('username')
    if not username:
        result = {'code':20103,'error':'Please give me username !'}
        return JsonResponse(result)
    password = json_obj.get('password')
    if not password:
        result = {'code': 20104, 'error': 'Please give me password !'}
        return JsonResponse(result)
    # 找用户
    users = UserProfile.objects.filter(username=username)
    if not users:
        result = {'code': 20105, 'error': 'The username or password is error !'}
        return JsonResponse(result)
    m5 = hashlib.md5()
    m5.update(password.encode())
    password_m5 = m5.hexdigest()
    user = users[0]
    if password_m5 != user.password:
        result = {'code': 20106, 'error': 'The username or password is error !'}
        return JsonResponse(result)
    # 生成token
    now_datetime = datetime.datetime.now()
    user.login_time = now_datetime
    user.save()
    token = make_token(username,now_datetime,86400)
    result = {'code':200,'data':{'token':token.decode()},'username':username}
    return JsonResponse(result)
