from django.urls import path, re_path
from account import views
 
urlpatterns = [
    re_path('login/', views.login),
    re_path('permission/', views.permission),
    re_path('logout/', views.logout),
    re_path('download/', views.Download), #未区分简易下载
    re_path('download1/', views.Download1),
    re_path('upload/', views.Upload),
]