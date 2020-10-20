from django.contrib import admin

from django.urls import path, include

from . import views



urlpatterns = [

    # 将路由和视图函数关联起来

    path('scanhosts/', views.do_scanhosts, name='scanhosts'),

]