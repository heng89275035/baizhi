from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
import json
from loginapp.models import Writings as writs
from loginapp.models import Type as types


# Create your views here.
def index(request):
    username = request.COOKIES.get("username")
    if username:
        username = username.encode('latin-1').decode('utf-8')

    writ = writs.objects.all()
    type1 = types.objects.filter(level=1)
    type2 = types.objects.filter(level=2)
    number = int(request.GET.get('number', 1))
    pagt = Paginator(object_list=writ, per_page=4)
    if number not in pagt.page_range:
        number = 1
    writ = pagt.page(number)
    # url1 = 'http://127.0.0.1:8000/manage/index/'
    url1 = reverse('manage:index')
    dic={'writ': writ, 'type1': type1, 'type2': type2,
                   'url1': url1,'username':username}
    return render(request, 'manage/index.html',dic)


def base(request):
    username = request.COOKIES.get("username")
    if username:
        username = username.encode('latin-1').decode('utf-8')

    level = request.GET.get('level')
    id = request.GET.get('id')
    if level == None or '':
        level =0
    if id == None or '':
        id =0
    type1 = types.objects.filter(level=1)
    type2 = types.objects.filter(level=2)
    ride_time = request.GET.get('ride_time')
    ride_type = request.GET.get('ride_type')
    ride_count = request.GET.get('ride_count')
    if ride_time == None:
        ride_time = 0
    if ride_count == None:
        ride_count = 0
    if ride_type == None:
        ride_type = 2
    ride_time = int(ride_time)
    ride_type = int(ride_type)
    ride_count = int(ride_count)

    print('接收时，ride_time=', ride_time)
    print('接收时，ride_type=', ride_type)
    print('接收时，ride_count=', ride_count)

    if ride_type == 1:
        ride_time += 1
    if ride_time == 2:
        ride_time = 0
    if ride_time >= 4:
        ride_time = 0

    if ride_type == 1:
        ride_count += 1
    if ride_count == 2:
        ride_count = 0
    if ride_count >= 4:
        ride_count = 0

    number = int(request.GET.get('number', 1))
    print('判断时，ride_time=', ride_time)
    print('判断时，ride_type=', ride_type)
    print('判断时，ride_count=', ride_count)
    if ride_type == 2:
        if level == '0':
            writ = writs.objects.all()
        elif level == '1':
            writ = writs.objects.filter(cate__parent_id=id)
        # elif level == '2':
        else:
            writ = writs.objects.filter(cate_id=id)
    elif ride_type == 1:

        if level == '0':
            writ = writs.objects.all()
            if ride_time == 1:
                writ = writs.objects.all().order_by('time')
            elif ride_time == 0:
                writ = writs.objects.all().order_by('-time')
            if ride_count == 1:
                writ = writs.objects.all().order_by('count')
            elif ride_count == 0:
                writ = writs.objects.all().order_by('-count')


        elif level == '1':
            writ = writs.objects.filter(cate__parent_id=id)
            if ride_time == 1:
                writ = writs.objects.filter(cate__parent_id=id).order_by('time')
            elif ride_time == 0:
                writ = writs.objects.filter(cate__parent_id=id).order_by('-time')
            if ride_count == 1:
                writ = writs.objects.filter(cate__parent_id=id).order_by('count')
            elif ride_count == 0:
                writ = writs.objects.filter(cate__parent_id=id).order_by('-count')


        # elif level == '2':
        else:
            writ = writs.objects.filter(cate_id=id)
            if ride_time == 1:
                writ = writs.objects.filter(cate_id=id).order_by('time')
            elif ride_time == 0:
                writ = writs.objects.filter(cate_id=id).order_by('-time')
            if ride_count == 1:
                writ = writs.objects.filter(cate_id=id).order_by('count')
            elif ride_count == 0:
                writ = writs.objects.filter(cate_id=id).order_by('-count')
    else:
        if level == '0':
            writ = writs.objects.all()
            if ride_time == 1:
                writ = writs.objects.all().order_by('time')
            elif ride_time == 0:
                writ = writs.objects.all().order_by('-time')
            if ride_count == 1:
                writ = writs.objects.all().order_by('count')
            elif ride_count == 0:
                writ = writs.objects.all().order_by('-count')


        elif level == '1':
            writ = writs.objects.filter(cate__parent_id=id)
            if ride_time == 1:
                writ = writs.objects.filter(cate__parent_id=id).order_by('time')
            elif ride_time == 0:
                writ = writs.objects.filter(cate__parent_id=id).order_by('-time')
            if ride_count == 1:
                writ = writs.objects.filter(cate__parent_id=id).order_by('count')
            elif ride_count == 0:
                writ = writs.objects.filter(cate__parent_id=id).order_by('-count')


        # elif level == '2':
        else:
            writ = writs.objects.filter(cate_id=id)
            if ride_time == 1:
                writ = writs.objects.filter(cate_id=id).order_by('time')
            elif ride_time == 0:
                writ = writs.objects.filter(cate_id=id).order_by('-time')
            if ride_count == 1:
                writ = writs.objects.filter(cate_id=id).order_by('count')
            elif ride_count == 0:
                writ = writs.objects.filter(cate_id=id).order_by('-count')

    pagt = Paginator(object_list=writ, per_page=4)
    if number not in pagt.page_range:
        number = 1
    writ = pagt.page(number)
    url1 = reverse('manage:base') + "?level=" + level + "&id=" + id
    id = int(id)

    ride_time = str(ride_time)
    ride_type = str(ride_type)
    print('结束时，ride_time=', ride_time)
    print('结束时，ride_type=', ride_type)
    print('结束时，ride_count=', ride_count)
    dic={'writ': writ, 'type1': type1, 'type2': type2
                      , 'id': id, 'level': level, 'url1': url1,
                   'number': number, "ride_time": ride_time,
                   'ride_count': ride_count, 'ride_type': ride_type,
                   'username':username}

    return render(request, 'manage/pythonBase.html',dic)


#
def delete(request):
    try:
        level = request.GET.get("level")
        id = request.GET.get("id")
        delete_id = request.GET.get("dele_id")
        number = request.GET.get("number")
        writ = writs.objects.filter(course_id=int(delete_id))
        print(level, id, delete_id)
        print(writ)
        with transaction.atomic():
            writ.delete()
            url = reverse('manage:base') + "?level=" + level + "&id=" + id + "&number=" + number
            return redirect(url)
    except:
        return HttpResponse("报错保护，请联系管理员")


def update(request):
    username = request.COOKIES.get("username")
    if username:
        username = username.encode('latin-1').decode('utf-8')

    course_id = request.GET.get('id')
    level = request.GET.get('level')
    id = request.GET.get('cate_id')
    number = request.GET.get("number")
    if number:
        number = request.GET.get("number")
    else:
        number = '1'
    writ = writs.objects.all()
    type1 = types.objects.filter(level=1)
    type2 = types.objects.filter(level=2)
    title = writs.objects.get(course_id=course_id).course_name
    # 默认选中的二级标题
    a = types.objects.get(id=id)
    # 默认选择的一级标题
    tt = types.objects.get(id=a.parent_id)
    content = writs.objects.get(course_id=course_id).content
    url = reverse('manage:base') + "?level=" + level + "&id=" + id + "&number=" + number
    url1=reverse('manage:base')
    dic = {'writ': writ, 'type1': type1, 'type2': type2,
           'title': title, 'id': id, 'course_id': course_id,
           'tt': tt, 't1': a, 'content': content, 'url': url, 'level': level,
           'number': number,'username':username,'url1':url1}

    return render(request, 'manage/update.html', dic)


def sel2(request):
    list = []
    title1 = request.POST.get('sel')
    type1_id = types.objects.get(title=title1).id
    type2 = types.objects.filter(parent_id=type1_id)
    for i in type2:
        list.append(i.title)

    return HttpResponse(json.dumps(list), content_type='application/json')


def update_submit(request):
    title = request.POST.get('title')
    type1 = request.POST.get('type1')
    type2 = request.POST.get('type2')
    content = request.POST.get('content')
    time = request.POST.get('time')
    course_id = request.POST.get('course_id')
    cate_id = types.objects.get(title=type2).id


    # 需要修改的文章
    title1 = writs.objects.get(course_id=course_id)
    with transaction.atomic():
        title1.course_name = title
        title1.content = content
        title1.time = time
        title1.cate_id = cate_id
        title1.save()
    # url = reverse('manage:base') + "?level=" + level + "&id=" + id + "&number=" + number
    return HttpResponse('修改成功')


def addCourse(request):
    username = request.COOKIES.get("username")
    if username:
        username = username.encode('latin-1').decode('utf-8')

    type1 = types.objects.filter(level=1)
    type2 = types.objects.filter(level=2)
    dict = {'type1': type1, 'type2': type2,'username':username}
    return render(request, 'manage/addCourse.html', dict)


def addCourse_add(request):
    try:
        titlename = request.POST.get('titlename')
        level = request.POST.get('level')
        typename = request.POST.get('typename')
        parent_id = types.objects.get(title=typename).id
        checkname = types.objects.filter(title=titlename)
        if checkname:
            return HttpResponse('名称重复')
        with transaction.atomic():
            if level == '1':
                types.objects.create(title=titlename, level=int(level), parent_id=0)
                id = types.objects.get(title=titlename).id
                return HttpResponse(id)
            elif level == '2':
                types.objects.create(title=titlename, level=int(level), parent_id=parent_id)
                id = types.objects.get(title=titlename).id
                return HttpResponse(id)

    except:
        return HttpResponse('出错了')


def addArticle(request):
    username = request.COOKIES.get("username")
    if username:
        username = username.encode('latin-1').decode('utf-8')
    type1 = types.objects.filter(level=1)
    type2 = types.objects.filter(level=2)
    writ = writs.objects.all()
    dict = {'type1': type1, 'type2': type2, 'writ': writ,'username':username}

    return render(request, 'manage/addArticle.html', dict)


def addArticle_submit(request):
    title = request.POST.get('title')
    type1 = request.POST.get('type1')
    type2 = request.POST.get('type2')
    time = request.POST.get('time')
    content = request.POST.get('content')
    checkname = writs.objects.filter(course_name=title)
    parent_id = types.objects.get(title=type2).id
    if checkname:
        return HttpResponse('名称重复')
    with transaction.atomic():
        writs.objects.create(time=time, content=content,
                             course_name=title, count=0, cate_id=parent_id)

        return HttpResponse('修改成功')


def quit_login(request):
    response=render(request, 'login/login.html')
    response.delete_cookie('username')
    return response

def login_out(request):
    return render(request, 'manage/logout.html')