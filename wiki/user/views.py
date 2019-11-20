import datetime
import json,jwt,hashlib
import time
from wtoken.views import make_token
from django.http import JsonResponse
from .models import UserProfile
from tools.logging_check import logging_check

# Create your views here.

@logging_check('PUT')
def users(request,username=None):

    if request.method == 'GET':
        if username:
            # 拿具体用户数据
            try:
                user = UserProfile.objects.get(username=username)
            except Exception as e:
                print(e)
                return JsonResponse({'code':10108,'error':'Not user'})
            # 有查询字符串【？nickname=1】
            if request.GET.keys():
                # 有查询字符串
                data = {}
                for k in request.GET.keys():
                    if hasattr(user,k):
                        # 过滤字段
                        if k == 'password':
                            continue
                        v = getattr(user,k)
                        data[k] = v
                res = {'code':200,'username':user.username,'data':data}
            else:
                # 无查询字符串
                user_data = {}
                user_data['nickname'] = user.nickname
                user_data['sign'] = user.sign
                user_data['info'] = user.info
                user_data['avatar'] = str(user.avatar)
                res = {'code':200,'username':user.username,'data':user_data}
            return JsonResponse(res)

        else:
            # 拿所有用户数据
            all_users = UserProfile.objects.all()
            users_data = []
            for user in all_users:
                user_dict = {}
                user_dict['username'] = user.username
                user_dict['nickname'] = user.nickname
                user_dict['sign'] = user.sign
                user_dict['info'] = user.info
                users_data.append(user_dict)
            res = {'code':200,'data':users_data}
            return JsonResponse(res)


    elif request.method == 'POST':
        # 创建用户
        json_str = request.body
        if not json_str:
            result = {'code': 10101, 'error': 'Please give me data !'}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        username = json_obj.get('username')
        if not username:
            result = {'code':10102,'error':'Please give me username !'}
            return JsonResponse(result)
        email = json_obj.get('email')
        if not email:
            result = {'code': 10103, 'error': 'Please give me email !'}
            return JsonResponse(result)
        password_1 = json_obj.get('password_1')
        password_2 = json_obj.get('password_2')
        if password_1 != password_2:
            result = {'code': 10104, 'error': 'The two password entries are not equal !'}
            return JsonResponse(result)

        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            result = {'code': 10105, 'error': 'The username is already existed !'}
            return JsonResponse(result)
        # 生成散列密码
        m5=hashlib.md5()
        m5.update(password_1.encode())
        password=m5.hexdigest()
        # 创建用户
        try:
            user = UserProfile.objects.create(username=username,nickname=username,email=email,password=password)
        except Exception as e:
            print('-----create error-----')
            print(e)
            result = {'code': 10106, 'error': 'The username is already existed !!'}
            return JsonResponse(result)
        # 可以生成令牌
        now_datetime = datetime.datetime.now()
        user.login_time = now_datetime
        user.save()
        token = make_token(username,now_datetime,86400)
        result = {'code':200,'data':{'token':token.decode()},'username':username}
        return JsonResponse(result)


    elif request.method == 'PUT':
        # 更新数据？
        # http://127.0.0.1:8000/v1/users/caoxudong
        if not username:
            res = {'code':10107,'error':'Must be give me username'}
            return JsonResponse(res)

        json_str = request.body
        #TODO 空body判断
        json_obj = json.loads(json_str)
        # TODO 判断是否有值
        nickname = json_obj.get('nickname')
        sign = json_obj.get('sign')
        info = json_obj.get('info')
        # 获取用户
        # users = UserProfile.objects.filter(username=username)
        # user = users[0]
        user = request.user
        # 当前请求 token用户 修改自己的数据
        if user.username != username:
            result = {'code':10108,'error':'The username is error !'}
            return JsonResponse(result)

        if user.nickname != nickname:
            user.nickname = nickname
        if user.info != info:
            user.info = info
        if user.sign != sign:
            user.sign = sign
        user.save()
        res = {'code':200,'username':username}
        return JsonResponse(res)


@logging_check('POST')
def users_avatar(request,username):
    # 处理头像上传
    if request.method != 'POST':
        result = {'code':10109,'error':'Please use POST !'}
        return JsonResponse(result)
    user = request.user
    if user.username != username:
        result = {'code': 10110, 'error': 'The username is error !'}
        return JsonResponse(result)

    user.avatar = request.FILES['avatar']
    user.save()
    return JsonResponse({'code':200,'username':username})

