from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.generic import TemplateView
from . import views
from . import admin_views

urlpatterns = [
    re_path('login/', views.login),
    re_path('logout/', views.logout),
    re_path('register/', views.register),
    re_path('getinfo/', views.getinfo),
    re_path('changeavatar/', views.change_avatar),
    re_path('certification_apply/', views.certification_apply),
    re_path('certification_list/', views.certification_list),
    re_path('unfinished_list/', views.unfinished_list),
    re_path('unfinished_detail/', views.unfinished_detail),
    re_path('finished_apply/', views.finished_apply),
    re_path('download_key/', views.download_key),
    re_path('certification_upload/', views.certification_upload),
    re_path('judge_upload/', views.judge_upload),
    re_path('judge_apply/', views.judge_apply),
    re_path('judge_list/', views.judge_list),
    re_path('get_count/', admin_views.get_count)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)