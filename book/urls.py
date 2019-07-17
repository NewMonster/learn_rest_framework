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

from django.conf.urls import url,include
from rest_framework import routers
from . import views

routers=routers.DefaultRouter()


routers.register(r'books',views.BooksModelviewset)


urlpatterns = [
    url(r"",include(routers.urls)),
    # url(r'^books/$',views.BooksModelviewset.as_view({'get':'list','post':'create'}),name='books_list'),
    url(r'^books/bid=(?P<pk>\d+)/$',views.BooksModelviewset.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'}),name='book_detail'),
    url(r'^authors/$',views.Authorsview.as_view(),name='authors_list'),
    url(r'^authors/aid=(?P<pk>\d+)/$',views.AuthorsDetailview.as_view(),name='author_detail'),
    url(r'^authors/bid=(?P<pk>\d+)/$',views.BookToAuthorview.as_view(),name='book_author'),
    url(r'^publishers/$',views.Publishersview.as_view(),name='publishers_list'),
    url(r'^publishers/pid=(?P<pk>\d+)/$', views.PublishersDetailview.as_view(),name='publisher_detail'),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
]
