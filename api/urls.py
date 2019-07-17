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
from django.contrib import admin
from rest_framework import routers
from . import views

routers=routers.DefaultRouter()

routers.register(r'xxx',views.FriendsModelviewset)
routers.register(r'rt',views.FriendsModelviewset)


urlpatterns = [
    url(r'^auth/$',views.Authview.as_view()),
    url(r'^order/$',views.OrderView.as_view()),
    url(r'^info/$',views.UserinfoView.as_view()),
    url(r'^index/$',views.Indexview.as_view()),
    # url(r'^users/$',views.Usersview.as_view()),
    url(r'^(?P<version>[v1|v2]+)/users/$',views.Usersview.as_view(),name="uuu"),
    url(r'^file/$',views.Fileview.as_view()),
    url(r'^roles/$', views.Rolesview.as_view()),
    url(r'^roles/user_id=(?P<user_id>\d+)/$',views.Rolesview.as_view(),name="roles"),
    url(r'^friends/$',views.Friendsview.as_view()),
    url(r'^groups/$',views.Groupsview.as_view()),
    url(r'^groups/group_id=(?P<group_id>\d+)/$',views.Groupsview.as_view(),name='group'),
    # url(r'^friends_gnc/$', views.FriendsGNCview.as_view()),
    # url(r'^friends_gncviewset/$', views.FriendsGNCviewset.as_view({'get':'list','post':'create'})),
    url(r'^friends_gnc/$', views.FriendsModelviewset.as_view({'get':'list','post':'create'})),
    url(r'^friends_gnc/user_id=(?P<pk>\d+)/$', views.FriendsModelviewset.as_view({'get': 'retrieve',
                                                'delete': 'destroy','put':'update','patch':'partial_update'})),

    # 自动生成4个url,一般选择使用
    url(r'',include(routers.urls)),

]

"""
   ^api/ ^xxx/$                                        [name='friends-list']
   ^api/ ^xxx\.(?P<format>[a-z0-9]+)/?$                [name='friends-list']
   ^api/ ^xxx/(?P<pk>[^/.]+)/$                         [name='friends-detail']
   ^api/ ^xxx/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='friends-detail']
   ^api/ ^rt/$                                         [name='friends-list']
   ^api/ ^rt\.(?P<format>[a-z0-9]+)/?$                  [name='friends-list']
   ^api/ ^rt/(?P<pk>[^/.]+)/$                           [name='friends-detail']
   ^api/ ^rt/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$   [name='friends-detail']
"""