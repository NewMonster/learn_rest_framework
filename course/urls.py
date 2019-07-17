#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@Software: PyCharm
@Author  : cn
@Email   : chenningxj@163.com
@File    : urls.py
@Time    : 2019-7-16 下午9:05
@version : v1.0
"""



from django.conf.urls import url,include
from django.contrib import admin

from course import views


urlpatterns = [
    url(r'^test/$',views.test),

]







































