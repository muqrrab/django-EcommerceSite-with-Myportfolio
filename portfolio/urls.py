from django.urls import path, re_path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('resume', views.df, name="df"),
    path('formsubmission/', views.formsubmission, name="formsubmission"),
    # re_path(r"^home/", include("home.urls"),name="home"),
]
