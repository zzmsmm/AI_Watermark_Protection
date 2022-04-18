from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('login/',views.login, name='login'),
    path('register/',views.register, name='register'),
]