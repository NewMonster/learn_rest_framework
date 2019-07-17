#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@Software: PyCharm
@Author  : cn
@Email   : chenningxj@163.com
@File    : pagernation.py
@Time    : 2019-7-13 下午5:51
@version : v1.0
"""


# 分页
from rest_framework.pagination import PageNumberPagination

# 自定义分页处理类
class MyPageNumberPagination(PageNumberPagination):
    # 默认每页显示是多少数据
    page_size = 2
    # 可以通过用户传过来的参数表示每页显示数据的大小  176.234.2.113:8000/api/friends/?page=1&page_size=10
    page_size_query_param = "page_size"    #
    # 设定用户传过来的请求显示数据的最大数量不可超过20
    max_page_size = 20

    # 请求页面的页面数的键为page(默认位page)   pn=4
    page_query_param = 'pn'



from rest_framework.pagination import LimitOffsetPagination
from Test01 import settings



class MyLimitOffsetPagination(LimitOffsetPagination):
    # 默认显示的每页数据数量
    default_limit = settings.REST_FRAMEWORK.get("PAGE_SIZE",2)
    # 钱端url上显示自定义数据数量的键
    limit_query_param = 'limit'

    # 钱端url定义偏移数据(从哪开始显示)的位置的键
    offset_query_param = 'offset'

    # 定义每页最大显示的数据条数
    max_limit = 20


from rest_framework.pagination import CursorPagination


class MyCursorPagination(CursorPagination):
    # 定义页面数量所显示的键
    cursor_query_param = 'cursor'

    # 默认的显示数据数量
    page_size = settings.REST_FRAMEWORK.get("PAGE_SIZE",2)

    # 定义的排序显示规则
    ordering = 'id'

    # 用户可通过此字段定义每页显示的数据数量
    page_size_query_param = "page_size"

    # 设置每页可显示数据的最大数量
    max_page_size = 20




























