from django.test import TestCase
from django.shortcuts import render
from django.http import HttpResponse
from loginapp.models import User as users
from loginapp.captcha.image import ImageCaptcha
import string, random

def get_cap(request):
    image = ImageCaptcha()
    code = random.sample(string.ascii_letters + string.digits, 4)
    code = ''.join(code)
    date = image.generate(code)  # 将字符写入图片中
    request.session['code'] = code
    print(code)
    return HttpResponse(date, 'image/png')


get_cap()
