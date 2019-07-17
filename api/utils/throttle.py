#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@Software: PyCharm
@Author  : cn
@Email   : chenningxj@163.com
@File    : throttle.py
@Time    : 2019-7-9 下午8:06
@version : v1.0
"""
from Test01.settings import *
from rest_framework.throttling import BaseThrottle,SimpleRateThrottle
import time

"""
VISIT_RECODE={}

class VisitedThrottle(BaseThrottle):
    # 限制用户访问频率
    def __init__(self):
        self.remote_addr=None
        self.throttle=THROTTLE_FREQUENCE   # 表示20秒可以访问三次


    def allow_request(self,request,view):
        # 1. 获取用户ip地址
        remote_addr = self.get_ident(request)
        self.remote_addr=remote_addr
        ctime=time.time()
        if remote_addr not in VISIT_RECODE:
            VISIT_RECODE[remote_addr]=[ctime,]
            return True
        history=VISIT_RECODE[remote_addr]
        self.history=history

        while history and history[-1]<ctime-self.throttle[0]:
            history.pop()

        if len(history)<self.throttle[1]:
            history.insert(0,ctime)
            return True    # 返回True表示可以继续访问
        return False   # 返回False表示访问频率过高,被限制


    def wait(self):
        # 还需等待多长时间可以访问
        history = VISIT_RECODE[self.remote_addr]
        ctime=time.time()
        need=self.throttle[0]-(ctime-history[-1])
        return need
"""


# 对于未登录用户的限流类
class VisitedThrottle(SimpleRateThrottle):
    scope = "lufei"
    def get_cache_key(self, request, view):
        # 如果已登录用户.则跳过验证
        if not request.user:
            return self.get_ident(request)


# 对于登录用户的限流类
class UserThrottle(SimpleRateThrottle):
    scope = "lufei_user"
    def get_cache_key(self, request, view):
        if request.user:
            return request.user.username

































