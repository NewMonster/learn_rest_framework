#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@Software: PyCharm
@Author  : cn
@Email   : chenningxj@163.com
@File    : auth.py
@Time    : 19-7-8 下午8:34
@version : v1.0
"""


from api.models import Users,UserToken
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


class Authentication(BaseAuthentication):
    def authenticate(self,request):
        token=request.GET.get("token")
        token_obj=UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("用户认证失败")
        # rest_framework内部会将两个字段赋值给request,以供后续操作使用
        return (token_obj.user,token_obj)


    def authenticate_header(self, request):
        pass




class FirstAuthtication(BaseAuthentication):
    def authenticate(self,request):
        pass


    def authenticate_header(self, request):
        pass




































