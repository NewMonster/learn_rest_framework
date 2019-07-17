#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@Software: PyCharm
@Author  : cn
@Email   : chenningxj@163.com
@File    : urls.py
@Time    : 19-7-6 下午8:28
@version : v1.0
"""


from django.conf.urls import url
from rest_framework import routers
from . import views

routers=routers.DefaultRouter()

# routers.register(r'xxx',views.FriendsModelviewset)
# routers.register(r'rt',views.FriendsModelviewset)


urlpatterns = [
    url(r'^books/$',views.Booksview.as_view(),name='books_list'),
    url(r'^books/bid=(?P<pk>\d+)/$',views.BooksDetailview.as_view(),name='book_detail'),
    url(r'^authors/$',views.Authorsview.as_view(),name='authors_list'),
    url(r'^authors/aid=(?P<pk>\d+)/$',views.AuthorsDetailview.as_view(),name='author_detail'),
    url(r'^authors/bid=(?P<pk>\d+)/$',views.BookToAuthorview.as_view(),name='book_author'),
    url(r'^publishers/$',views.Publishersview.as_view(),name='publishers_list'),
    url(r'^publishers/pid=(?P<pk>\d+)/$', views.PublishersDetailview.as_view(),name='publisher_detail'),
]
