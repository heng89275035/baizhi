from django.urls import path
from loginapp import views

app_name = 'login'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('reg/', views.reg, name='reg'),
    path('check_name/', views.check_name, name='check_name'),
    path('get_cap/', views.get_cap, name='get_cap'),
    path('check_register/', views.check_register, name='check_register'),
    path('login_in/', views.login_in, name='login_in'),
    path('active/', views.active, name='active'),
    path('again_active/', views.again_active, name='again_active'),
    path('forget_pwd/', views.forget_pwd, name='forget_pwd'),
    path('sub_forget_pwd/', views.sub_forget_pwd, name='sub_forget_pwd'),

]
