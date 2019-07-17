from api.models import Users,UserToken
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from django.http import HttpResponse
import hashlib
import time,json
from api.utils.permission import *
from api.utils.throttle import *
from django.shortcuts import render
from api.models import Friends
from api import models
from rest_framework.response import Response



# 创建token
def md5_create(user):
    ctime=str(time.time())
    m=hashlib.md5(bytes(user,encoding='utf-8'))
    m.update(bytes(ctime,encoding='utf-8'))
    print(m.hexdigest())
    return m.hexdigest()



from rest_framework.versioning import BaseVersioning


class ParamsVersion(object):
    def determine_version(self, request, *args, **kwargs):
        version=request.query_params.get('version')
        return version





class Authview(APIView):
    """
        用于用户登录认证
    """
    # 登录取消认证
    authentication_classes = []
    # 权限认证为空
    permission_classes = []
    # 限流设置   特殊视图通过ip进行限制
    throttle_classes = [VisitedThrottle, ]

    def post(self,request,*args,**kwargs):
        dic={"code":1000,"msg":None}
        try:
            uname=request._request.POST.get('username')
            pwd=request._request.POST.get('password')
            print(request._request.GET)
            print(uname,pwd)
            user_obj=Users.objects.filter(username=uname,password=pwd).first()
            # 未登录用户创建一个token md5加密时间戳+用户名
            if not user_obj:
                dic["code"]=1001
                dic["msg"]='用户名或密码错误'
            token=md5_create(uname)
            # 存在就更新不在就创建
            UserToken.objects.update_or_create(user=user_obj,defaults={"token":token})
            dic["token"]=token
        except Exception as e:
            print(e)
            dic["code"] = 1002
            dic["msg"] = '请求异常'
        return Response(json.dumps(dic))



ORDER_DICT={
    1:{
        "name":"媳妇",
        "age":"18",
        "性别":"男",
        "content":"...."
    },
    2:{
        "name":"dog",
        "age":"2",
        "性别":"男",
        "content":"...."
    }

}


class OrderView(APIView):
    """
        用于订单相关业务(svip有权限)
    """
    # 认证,验证用户是否登录,如果成功返回元组:(用户对象,token/认证信息),如果认证失败,则抛出异常
    # authentication_classes = [Authentication,]  # 在settings里已经设置全局认证

    # 权限认证,确认用户是否有权限访问此视图函数   全局实现
    permission_classes = [SVIPpermission,]

    def get(self,request,*args,**kwargs):
        # 权限的实现
        # if request.user.user_type!=3:
        #     return HttpResponse("无权访问")
        ret={"code":1000,"msg":None,"data":None}
        # token=request._request.GET.get('token')
        # if not token:
        #     ret['msg']='用户未登录'
        #     ret['code']=1004
        #     return JsonResponse(ret)
        try:
            ret['data']=ORDER_DICT

        except Exception as e:
            pass

        return JsonResponse(ret)




class UserinfoView(APIView):
    """
        用户信息(普通用户和vip用户有权限)
    """
    # 认证,验证用户是否登录,如果成功返回元组:(用户对象,token/认证信息),如果认证失败,则抛出异常
    # authentication_classes = [Authentication,]    # 在settings里已经设置全局认证

    # 权限认证,确认用户是否有权限访问此视图函数
    permission_classes = [permission, ]

    def get(self,request,*args,**kwargs):
        return HttpResponse("用户信息")


GOODS_DICT={
    1:{
        "name":"苹果",
        "price":"18",
        "storge":"4556",
        "content":"...."
    },
    2:{
        "name":"dog",
        "price":"28",
        "storge":"45",
        "content":"...."
    }

}

from api.utils.throttle import VisitedThrottle

class Indexview(APIView):
    """
        主页视图
    """
    authentication_classes = []
    permission_classes = []
    # 限流设置   特殊视图通过ip进行限制
    throttle_classes = [VisitedThrottle,]

    def get(self,request,*args,**kwargs):
        return JsonResponse(GOODS_DICT)


from rest_framework.parsers import JSONParser,FormParser,MultiPartParser,FileUploadParser


class Usersview(APIView):
    # 认证
    authentication_classes = []
    # 权限
    permission_classes = []
    # 限流
    throttle_classes = [VisitedThrottle,]
    # 版本   全局配置URLPathVersioning
    # versioning_class=URLPathVersioning
    # 解析器     全局配置,入个别视图需要上传文件,则设置FileUploadParser
    # parser_classes = [JSONParser,FormParser]

    def get(self,request,*args,**kwargs):
        print(request.version)   # 获取版本
        print(request.versioning_scheme)    # 获取版本处理类
        # 反向生成url
        # print(request.versioning_scheme.reverse("uuu",request=request))

        return HttpResponse("用户列表")


    def post(self,request,*args,**kwargs):
        from rest_framework.request import Request
        print(request.data)
        print(request._request.POST)
        return HttpResponse("request.POST和request.data")



class Fileview(APIView):
    # 认证
    authentication_classes = []
    # 权限
    permission_classes = []
    # 限流
    throttle_classes = [VisitedThrottle,]
    # 版本   全局配置URLPathVersioning
    # versioning_class=URLPathVersioning
    # 解析器     全局配置,入个别视图需要上传文件,则设置FileUploadParser
    parser_classes = [MultiPartParser,FileUploadParser]

    def get(self,request,*args,**kwargs):
        print(request.version)   # 获取版本
        print(request.versioning_scheme)    # 获取版本处理类
        # 反向生成url
        return render(request,'file.html')

    # 上传文件
    def post(self,request,*args,**kwargs):
        print(request.content_type)
        # 获取请求的值，并使用对应的JSONParser进行处理
        print(request.data)
        # application/x-www-form-urlencoded 或 multipart/form-data时，request.POST中才有值
        print(request.POST)
        print(request.FILES)
        file=request.FILES.get("img")
        filename=MEDIA_ROOT+file.name
        print(MEDIA_ROOT,filename)
        with open(filename,'wb') as f:
            f.write(file.file.read())
        return HttpResponse("request.POST和request.data")


from api.models import Roles
from rest_framework import serializers
from rest_framework import exceptions

# 序列化继承自serializers.Serializer,需要自定义字段显示(字段名称必须有数据库字段一直)
class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Roles
        fields=['id','title']
        depth=0


class Rolesview(APIView):
    # 认证
    authentication_classes = []
    # 权限
    permission_classes = []
    # 限流
    throttle_classes = [VisitedThrottle,]
    # 版本   全局配置URLPathVersioning
    # versioning_class=URLPathVersioning
    # 解析器     全局配置,入个别视图需要上传文件,则设置FileUploadParser
    # parser_classes = [FormParser,JSONParser]

    def get(self,request,*args,**kwargs):
        # roles=Roles.objects.all().values('id','title')
        # print(roles,type(roles))
        # roles=list(roles)
        # ret=json.dumps(roles,ensure_ascii=False)

        # 单个对象的序列化
        # roles = Roles.objects.first()
        # ser = RolesSerializer(instance=roles, many=False)
        # 多个对象的序列化
        pk=kwargs.get("user_id",None)
        roles= Roles.objects.all()
        ser = RolesSerializer(instance=roles, many=True)
        if pk:
            user=models.Friends.objects.filter(pk=pk).first()
            roles = Roles.objects.filter(friends=user).all()
            ser = RolesSerializer(instance=roles, many=True)
        # ser.data已经是转化完成的结果
        ret=json.dumps(ser.data,ensure_ascii=False)
        return HttpResponse(ret)


class FriendsSerializer(serializers.Serializer):
    name=serializers.CharField()
    # password=serializers.CharField()
    # xxx = serializers.CharField(source='user_type')    # 显示为数字
    # choicefield字段 使用 source='get_数据库字段_display'   --->choicefield字段的序列化
    ooo=serializers.CharField(source='get_user_type_display')
    # ForeignKey字段    -->外键字段的序列化
    group=serializers.CharField(source='group.title')
    # ManyToMany字段    --->SerializerMethodField() 再自定义get_开头值属性的函数确定输出数据
    roles=serializers.SerializerMethodField()
    # 通过在模型类中定义方法使用ListField实现
    # roles = serializers.ListField(source='get_friends_info')


    def get_roles(self,row):
        roles_object_list=row.roles.all()
        ret=[]
        for item in roles_object_list:
            ret.append({'id':item.id,"title":item.title})
        return ret


# 自定义类(不常用)
class Myfield(serializers.CharField):
    def to_representation(self,db_data):
        print(db_data)
        return "我是一只小羔羊"


# 继承自serializers.ModelSerializer的序列化类
class FriendsUpperSerializer(serializers.ModelSerializer):
    user_type=serializers.CharField(source='get_user_type_display')
    roles_list=serializers.SerializerMethodField()     # 自定义显示方法
    group = serializers.CharField(source='group.title')
    xxx1=Myfield(source="name")

    # 自定义关联的模型类和需要显示的字段
    class Meta:
        # 关联的模型类名
        model=Friends
        # 序列化的字段列表
        fields=['id','name','email','password','school','user_type','group','roles_list',"xxx1"]

    # 自定义方法
    def get_roles_list(self,friend):
        roles_object_list=friend.roles.all()
        ret=[]
        for item in roles_object_list:
            ret.append({'id':item.id,"title":item.title})
        return ret


# 验证用户名类
class UsernameValidator:
    def __init__(self):
        pass

    def __call__(self, value):
        user=models.Friends.objects.filter(name=value).first()
        if user:
            msg = '用户名重复'
            raise serializers.ValidationError(msg)

    def set_context(self,field):
        pass


# 自动序列化表
class FriendsLastSerializer(serializers.ModelSerializer):
    # view_name=路由视图别名,lookup_field=数据库字段,group_id=反向url中的参数键
    # group=serializers.HyperlinkedIdentityField(view_name='group',lookup_field='group_id',lookup_url_kwarg="group_id")
    # roles=serializers.HyperlinkedIdentityField(view_name='roles',lookup_url_kwarg="user_id")
    # # Choice字段要自己重新定义数据类型
    # # 字段校验
    # user_type=serializers.CharField(source='get_user_type_display',required=False)
    # name=serializers.CharField(max_length=5,
    #                            error_messages={"title":"姓名不能为空","max_length":"用户名不能超过5个字符"})
    # password=serializers.CharField(min_length=6,max_length=20,error_messages={"titile":"密码不能为空",
    #                                "max_length":"密码不能少于6个字符","min_length":"密码不能超过5个字符"})

    # 自定义关联的模型类和需要显示的字段
    class Meta:
        # 关联的模型类名
        model = Friends
        # 序列化的字段列表
        fields = ['id', 'name', 'email', 'password', 'school', 'user_type', 'group','roles','phone','age']
        # fields="__all__"
        depth=1     # 官方建议0~10之间,课程建议3以下可使用

    # def create(self, validated_data):
    #     # print(validated_data)
    #     friend=models.Friends.objects.create(
    #         name=validated_data["name"],school=validated_data["school"],age=validated_data["age"],user_type=validated_data.get("user_type",1),
    #         email=validated_data["email"],password=validated_data["password"],phone=validated_data["phone"])
    #     return friend


    # value表示从前端传来的待判定的数据(已通过自身定义字段类型的正则表达式验证)
    def validate_name(self, value):
        # 验证失败可返回一个ValidationError('xxx')异常
        # raise exceptions.ValidationError('这是不对的,嘤嘤嘤')
        return value

"""
分页:
    a.第一种:看第page页,每页显示page_size条数据
    b.第二种:在offset的位置,向后查看limit条数据
    c.第三种:基于加密的,只能查看上一页和下一页     数据量大,速度有优势    记住前面的位置,运用> limit实现
    # 在分页是由于需要扫描的跳过数据条数的数据大,导致越往后查看速度越慢
"""
from api.utils.pagernation import MyPageNumberPagination,MyCursorPagination
from rest_framework.pagination import LimitOffsetPagination,CursorPagination


class Friendsview(APIView):
    # 认证
    authentication_classes = []
    # 权限
    permission_classes = []
    # 限流
    throttle_classes = [VisitedThrottle,]
    # 版本   全局配置URLPathVersioning
    # versioning_class=URLPathVersioning
    # 解析器     全局配置,入个别视图需要上传文件,则设置FileUploadParser
    # parser_classes = [FormParser,JSONParser]


    def get(self,request,*args,**kwargs):
        # friend=Friends.objects.first()
        # print(friend.get_user_type_display())
        # print(friend.group.title)
        # print(friend.get_friends_info())
        friends=Friends.objects.all()
        # 创建序列化对象,执行自身的或基类的__new__()和__init__()方法,一直找到基类中此方法的父类,实现序列化
        # context={"request":request}在生成url时使用
        # 1. 实例化序列化对象 一般将传入的数据封装到对象,先执行__new__() 返回一个创建后的对象
        """如果many=True,返回ListSerializer对象,接下来执行自身或ListSerializer的__init__()方法"""
        """如果many=False,返回BaseSerializer对象,接下来执行自身或BaseSerializer的__init__()方法"""
        ser=FriendsLastSerializer(instance=friends,many=True,context={"request":request})
        # 调用对象的data属性
        """对于ListSerializer的data,调用父类data方法,在调用自身的to_representation方法"""
        """对于BaseSerializer的data,调用自身data方法,在调用自身的to_representation方法"""
        # ret=json.dumps(ser.data,ensure_ascii=False)
        # return HttpResponse(ret)

        # 创建分页对象,使用分页显示数据
        """第一种"""
        # pg=MyPageNumberPagination()      # url=176.234.2.113:8000/api/friends/?page=1&page_size=10
        """第二种"""
        # pg = LimitOffsetPagination()    # url=http://176.234.2.113:8000/api/friends/?limit=4&offset=6
        """第三种"""
        pg = MyCursorPagination()

        # 获取分页后的数据
        # queryset=从数据库拿去的全部要显示的数据,request=request,view=视图对象(self)
        page_roles =pg.paginate_queryset(queryset=friends,request=request,view=self)

        # 对分页后的数据进行序列化
        ser=FriendsLastSerializer(instance=page_roles,many=True)

        # 使用rest_framework的Response对象返回数据,使用渲染器
        # return Response(ser.data)

        # 使用pg.get_paginated_response(ser.data)在结果里上一个和下一个以及总共有多少数据的信息
        """
            "count": 35,
            "next": "http://176.234.2.113:8000/api/friends/?page_size=4&pn=3",
            "previous": "http://176.234.2.113:8000/api/friends/?page_size=4",
        """
        ret=pg.get_paginated_response(ser.data)
        return ret



    def post(self,request,*args,**kwargs):
        # print(request.data)
        # print(request.META.get('HTTP_ACCEPT'))     # application/json;version=v2
        # # 使用json发送数据,请求数据类型application/json,则request.POST里无数据
        # print(request.POST)
        # 验证数据
        ser=FriendsLastSerializer(data=request.data)
        # 验证数据
        if ser.is_valid():
            # print(ser.validated_data)
            ret=ser.save()
            print(ret)
            friends=FriendsLastSerializer(instance=ret,many=False)
            res=json.dumps(friends.data,ensure_ascii=False)
        else:
            res=json.dumps(ser.errors,ensure_ascii=False)
            print(res)
        return HttpResponse(res)




# 查看用户组的序列化类
class GroupSerializers(serializers.ModelSerializer):
    class Meta:
        model=models.UserGroup
        fields="__all__"


# 查看用户组信息的CBV
class Groupsview(APIView):
    # 认证
    authentication_classes = []
    # 权限
    permission_classes = []
    # 限流
    throttle_classes = [VisitedThrottle, ]

    def get(self, request, *args, **kwargs):
        group_obj = models.UserGroup.objects.all()
        ser = GroupSerializers(instance=group_obj, many=True)
        pk=kwargs.get('group_id',None)
        if pk:
            group_obj=models.UserGroup.objects.filter(pk=pk).first()
            ser=GroupSerializers(instance=group_obj,many=False)

        ret=json.dumps(ser.data,ensure_ascii=False)

        return HttpResponse(ret)


"""
from rest_framework.generics import GenericAPIView

class FriendsGNCview(GenericAPIView):
    # 认证
    authentication_classes = []
    # 查询数据
    queryset = models.Friends
    # 序列化
    serializer_class = FriendsLastSerializer
    # 分页
    pagination_class=LimitOffsetPagination


    def get(self,request,*args,**kwargs):
        # 获取对象
        fs = models.Friends.objects.all()
        # 分页
        fs_pg=self.paginate_queryset(fs)
        # 序列化
        ser=self.get_serializer(instance=fs_pg,many=True)
        ret=self.get_paginated_response(ser.data)
        return ret
        # return Response(ser.data)
"""

from rest_framework.viewsets import GenericViewSet

"""
class FriendsGNCviewset(GenericViewSet):
    # 认证
    authentication_classes = []
    # 查询数据
    queryset = models.Friends
    # 序列化
    serializer_class = FriendsLastSerializer
    # 分页
    pagination_class=LimitOffsetPagination


    def list(self,request,*args,**kwargs):
        # 获取对象
        fs = models.Friends.objects.all()
        # 分页
        fs_pg=self.paginate_queryset(fs)
        # 序列化
        ser=self.get_serializer(instance=fs_pg,many=True)
        ret=self.get_paginated_response(ser.data)
        return ret
    
    def submit(self,request,*args,**kwargs):
        return Response("接到数据")
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin
from api.utils.auth import Authentication
from rest_framework.renderers import JSONRenderer,BrowsableAPIRenderer


class FriendsModelviewset(ModelViewSet):
    # 认证
    authentication_classes = []
    # 查询数据
    queryset = models.Friends.objects.all()
    # 序列化
    serializer_class = FriendsLastSerializer
    # 分页
    pagination_class = LimitOffsetPagination
    # 解析器
    pagination_classes=[JSONParser,FormParser]
    # 认证
    permission_classes = []
    # 渲染器    # 全局设置
    # renderer_classes = [JSONRenderer,BrowsableAPIRenderer]





