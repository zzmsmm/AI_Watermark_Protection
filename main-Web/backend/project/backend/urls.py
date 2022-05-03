from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.generic import TemplateView

from . import views

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
    re_path('finished_apply/', views.finished_apply)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)