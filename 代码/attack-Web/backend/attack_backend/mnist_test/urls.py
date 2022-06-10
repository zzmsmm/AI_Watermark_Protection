from django.urls import path, re_path
from mnist_test import views
 
urlpatterns = [
    re_path('login/', views.login),
    re_path('permission/', views.permission),
    re_path('logout/', views.logout),
    re_path('download/', views.Download),
    re_path('download1/', views.Download1),
    re_path('upload/', views.Upload),
]