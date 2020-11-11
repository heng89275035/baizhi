from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class MyMiddleware(MiddlewareMixin):
    def __init__(self, get_response):  # 初始化
        super().__init__(get_response)


    # view处理请求前执行
    def process_request(self, request):  # 某一个view
        checked_url = [reverse('manage:index'),reverse('manage:base'),reverse('manage:update'),
                       reverse('manage:addArticle'),reverse('manage:addCourse')]
        if request.path in checked_url:
            is_login = request.session.get('is_login')
            username = request.COOKIES.get("username")
            if username:
                username = username.encode('latin-1').decode('utf-8')
            if is_login and username:
                pass
            else:
                return redirect('login:login')


    # # 在process_request之后View之前执行
    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     pass
    #     # print("view:", request, view_func, view_args, view_kwargs)
    #
    # # view执行之后，响应之前执行
    # def process_response(self, request, response):
    #     print("response:", request, response)
    #     return response  # 必须返回response
    # #
    # # 如果View中抛出了异常
    # def process_exception(self, request, ex):  # View中出现异常时执行
    #     pass
    #     # print("exception:", request, ex)