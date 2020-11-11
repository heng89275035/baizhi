from django.urls import path
from manageapp import views

app_name = 'manage'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('base/', views.base, name='base'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('sel2/', views.sel2, name='sel2'),
    path('update_submit/', views.update_submit, name='update_submit'),
    path('addCourse/', views.addCourse, name='addCourse'),
    path('addCourse_add/', views.addCourse_add, name='addCourse_add'),
    path('addArticle/', views.addArticle, name='addArticle'),
    path('addArticle_submit/', views.addArticle_submit, name='addArticle_submit'),
    path('quit_login/', views.quit_login, name='quit_login'),
    path('login_out/', views.login_out, name='login_out'),

]
