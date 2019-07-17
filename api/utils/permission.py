#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@Software: PyCharm
@Author  : cn
@Email   : chenningxj@163.com
@File    : permission.py
@Time    : 19-7-8 下午10:05
@version : v1.0
"""
from rest_framework.permissions import BasePermission

class SVIPpermission(BasePermission):
    """
        Svip权限实现类
    """
    message="必须是SVIP才能访问"
    def has_permission(self,request,view):
        if request.user.user_type!=3:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        return True


class permission(BasePermission):
    """
        未登录维护和vip和普松用户权限1实现类
    """
    def has_permission(self,request,view):
        if not request.user:
            return False
        print(request.user)
        if request.user.user_type in [1,2,3]:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if not request.user:
            return False
        print(request.user)
        if request.user.user_type in [1,2,3]:
            return True
        return False










































