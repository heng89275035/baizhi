import random
import re
import string
import hashlib
import traceback
import uuid

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from loginapp.models import User as users
from loginapp.captcha.image import ImageCaptcha
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.contrib.auth import settings

# Create your views here.


def reg(request):
    return render(request, 'login/register.html')


def check_name(request):
    username = request.POST.get('username')
    result = users.objects.filter(username=username).count()
    if result == 0:
        return HttpResponse('1')
    else:
        return HttpResponse('0')


def get_cap(request):
    image = ImageCaptcha()
    code = random.sample(string.ascii_letters + string.digits, 4)
    code = ''.join(code)
    date = image.generate(code)  # 将字符写入图片中
    request.session['code'] = code
    print('验证码是：', code)
    return HttpResponse(date, 'image/png')


def check_register(request):
    try:
        code = request.session['code']
        captcha = request.POST.get("captcha")
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        allow = request.POST.get("allow")
        # 后台验证信息是否合法
        name1 = re.match('^[\u4E00-\u9FA5]{2,10}$', username)
        password1 = re.match('^(\w){6,20}$', password)
        email1 = re.match('^\w+@[a-zA-Z0-9]{2,10}(?:\.[a-z]{2,4}){1,3}$', email)
        # 密码加密
        salt = str(uuid.uuid4())
        sha = hashlib.sha1()
        sha.update((password + salt).encode())
        pwd = sha.hexdigest()

        result = users.objects.filter(username=username)
        # 用户名重复
        if result:
            return HttpResponse('3')
        # 数据不合法
        if name1 == None or password1 == None or email1 == None:
            return HttpResponse('2')
        # 验证码错误
        if code != captcha:
            return HttpResponse('0')
        else:
            users.objects.create(username=username, password=pwd, email=email, is_active=0,salt=salt)
            # 发送激活邮件
            id=users.objects.get(username=username).id
            ser=Serializer(settings.SECRET_KEY,expires_in=180)
            resultid=ser.dumps({"id":id})
            send_mail('账号激活','用户 '+username+' 请求激活账号，激活链接为http://127.0.0.1:8000/login/active/?content='+resultid.decode(),'990014789@qq.com',['heng89275035@163.com','990014789@qq.com'])
            return HttpResponse('1')
    except:
        traceback.print_exc()
        return HttpResponse('5')


def active(request):
    try:
        content=request.GET.get('content')
        ser = Serializer(settings.SECRET_KEY, expires_in=180)
        id = ser.loads(content).get('id')
        user = users.objects.get(pk=id)
        user.is_active = 1
        user.save()
        return HttpResponse('激活成功')
    except:
        traceback.print_exc()
        return HttpResponse('激活失败，已过期')

def login_in(request):
    username = request.POST.get("username")
    pwd = request.POST.get("pwd")

    salt=users.objects.get(username=username).salt
    sha = hashlib.sha1()
    sha.update((pwd + salt).encode())
    pwd = sha.hexdigest()

    rem = request.POST.get("check")
    result = users.objects.filter(username=username, password=pwd)
    if result:
        active = users.objects.get(username=username).is_active
        if active == 0:
            return HttpResponse('2')
        request.session['is_login'] = True

        home = HttpResponse('1')
        if rem:
            username = username.encode('utf-8').decode('latin-1')
            home.set_cookie('username', username, max_age=3600 * 24 * 7)
            home.set_cookie('password', pwd, max_age=3600 * 24 * 7)
        else:
            username = username.encode('utf-8').decode('latin-1')
            home.set_cookie('username', username)
            home.set_cookie('password', pwd)
        return home
    else:
        result = users.objects.filter(username=username)
        result1 = users.objects.filter(password=pwd)
        if result:
            # 仅密码错误
            return HttpResponse('仅密码错误')
        elif result1:
            # 仅账号错误
            return HttpResponse('仅账号错误')
        else:
            return HttpResponse('账号密码都错')


def login(request):
    username = request.COOKIES.get("username")
    if username:
        username = username.encode('latin-1').decode('utf-8')
    password = request.COOKIES.get("password")
    a = users.objects.filter(username=username, password=password)
    if a:
        request.session['is_login'] = True
        return redirect('/manage/index/')
    return render(request, 'login/login.html')



def again_active(request):
    username=request.POST.get('username')
    pwd=request.POST.get('pwd')

    salt=users.objects.get(username=username).salt
    sha = hashlib.sha1()
    sha.update((pwd + salt).encode())
    pwd = sha.hexdigest()

    result = users.objects.filter(username=username, password=pwd)
    if result:
        id = users.objects.get(username=username).id
        ser = Serializer(settings.SECRET_KEY, expires_in=180)
        resultid = ser.dumps({"id": id})
        send_mail('账号激活',
                  '用户 ' + username + ' 请求激活账号，激活链接为http://127.0.0.1:8000/login/active/?content=' + resultid.decode(),
                  '990014789@qq.com', ['heng89275035@163.com', '990014789@qq.com'])
        return HttpResponse('1')
    else:
        return HttpResponse('1')


def forget_pwd(request):
    return render(request, 'login/forget_pwd.html')


def sub_forget_pwd(request):
    pass


