import jwt
from django.http import JsonResponse

from user.models import UserProfile


token_key = 'cxd'
def logging_check(*methods):
    def _logging_check(func):
        def wrapper(request,*args,**kwargs):
            # 逻辑判断
            # 1.判断当前请求是否需要校验
            # 2.取出token
            # 3.如果需要校验token,如何校验
            if not methods:
                return func(request,*args,**kwargs)
            else:
                if request.method not in methods:
                    return func(request,*args,**kwargs)
            # 取出token                    Authorization
            token = request.META.get('HTTP_AUTHORIZATION')
            if not token:
                result = {'code':20107,'error':'Please login !'}
                return JsonResponse(result)
            # 校验失败
            try:
                res = jwt.decode(token,token_key,algorithms='HS256')
            except Exception as e:
                result = {'code': 20108, 'error': 'Please login !'}
                return JsonResponse(result)

            username = res['username']

            try:
                user = UserProfile.objects.get(username=username)
            except Exception as e:
                print(e)
                return JsonResponse({'code':20109,'error':'Not user'})

            # 取出token里的login-time
            login_time = res.get('login_time')
            if login_time:
                if str(user.login_time)  != login_time:
                    result = {'code':20110,'error':'Other people have logined ! Please login again !'}
                    return JsonResponse(result)

            request.user = user

            return func(request,*args,**kwargs)
        return wrapper
    return _logging_check


def get_user_by_request(request):
    # 尝试获取用户身份
    # return user or none
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        # 用户没登录
        return None
    try:
        res = jwt.decode(token,token_key,algorithms='HS256')
    except Exception as e:
        return None
    username = res['username']
    users = UserProfile.objects.filter(username=username)
    if not users:
        return None
    user = users[0]
    return user