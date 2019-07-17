from django.shortcuts import render
from django.shortcuts import render, HttpResponse
from book import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.parsers import JSONParser,FormParser
from rest_framework.exceptions import ValidationError

import json

"""自定义序列化类(集成度底)"""
# 为queryset,model对象做序列化===》相当于form组件使用
# 这个可以放在一个单独的.py文件中
"""
class BookSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=32)
    price = serializers.IntegerField()
    pub_date = serializers.DateField()
    # 上面的只是针对的一对一字段的，若果用在一对多字段上的时候就会输出关联那张表的 def __str__(self)
    # publish = serializers.CharField()
    # 这个表示的是实现关联表中publish表中的name字段，可以自己定制
    publish = serializers.CharField(source="publish.name")
    # authors=serializers.CharField(source="authors.all")
    # 当出现多对多的时候上面的方式也不可行，上面会显示的是一个queryset对象
    # 自己定制显示什么
    authors = serializers.SerializerMethodField()

    def get_authors(self, obj):
        temp = []
        for obj in obj.authors.all():
            temp.append(obj.name)
        return temp

"""


"""全自动序列化类(集成度高)"""
# 为queryset,model对象做序列化===》相当于form组件使用
class BookModelSerializers(serializers.ModelSerializer):
    publish=serializers.HyperlinkedIdentityField(view_name='publisher_detail',lookup_field='publish_id',lookup_url_kwarg='pk')
    authors=serializers.HyperlinkedIdentityField(view_name='book_author',lookup_field='id',lookup_url_kwarg="pk")
    publish_id=serializers.IntegerField(default=1)
    class Meta:
        model=models.Book
        fields="__all__"
        depth=1

    # 方法名:validated_字段名,value参数表示前段传递的参数,
    # return要保存在数据库的值
    def validated_publish_id(self,value):
        print("value",value)
        return int(value)


# 书籍列表
class Booksview(APIView):
    # 认证
    authentication_classes = []
    # 解析器
    parser_classes =[JSONParser,FormParser]

    def get(self, request, *args, **kwargs):
        # 序列化
        # 方式一：
        # book_data = list(models.Book.objects.all())
        # print(book_data)
        # return HttpResponse(book_data)
        # 方式二：
        # from django.forms.models import model_to_dict
        # book_data = models.Book.objects.all()
        # temp = []
        # for obj in book_data:
        #     temp.append(model_to_dict(obj))
        # return HttpResponse(temp)
        # 方式三：
        # from django.core import serializers
        # book_data = models.Book.objects.all()
        # ret = serializers.serialize("json", book_data)
        # print(type(ret))
        # return HttpResponse(ret)
        # 方式四：序列组件
        # 这里面和Django里面的form组件和modelform组件相似
        # 这里记住要是使用浏览器访问的话这个必须要在setting中的INSTALLED_APPS注册rest_framework要不就会报错
        # 最好在项目一开始的时候就在setting里面注册
        book_data = models.Book.objects.all()
        # many=True 表示的queryset对象，反之many=False就表示为model对象相当于form组件
        # bs = BookSerializers(book_data, many=True)
        bs = BookModelSerializers(book_data, many=True,context={'request': request})
        return Response(bs.data)

    def post(self, request, *args, **kwargs):
        ser=BookModelSerializers(data=request.data)
        if ser.is_valid():
            res=ser.save()
            ret=BookModelSerializers(instance=res,many=False,context={'request': request})
        else:
            ret=ser.errors
        return Response(ret.data)

        # ser = BookModelSerializers(data=request.data)
        # # 验证数据
        # if ser.is_valid():
        #     ret = ser.save()
        #     res = BookModelSerializers(instance=ret, many=False,context={'request': request})
        # else:
        #     res =ser.errors
        # return Response(res.data)

# 单个书籍详细信息
class BooksDetailview(APIView):
    # 认证
    authentication_classes = []
    # 解析器
    parser_classes = [JSONParser, FormParser]

    def get(self, request, *args, **kwargs):
        pk=kwargs.get('pk')
        book_data = models.Book.objects.filter(pk=pk).first()
        bs = BookModelSerializers(book_data, many=False)
        return Response(bs.data)


# 作者序列化类
class AuthorsModelSerializers(serializers.ModelSerializer):
    class Meta:
        model=models.Author
        fields='__all__'
        depth=1


# 获取用户列表
class Authorsview(APIView):
    # 认证
    authentication_classes = []
    # 解析器
    parser_classes = [JSONParser, FormParser]

    def get(self, request, *args, **kwargs):
        author_data = models.Author.objects.all()
        bs = AuthorsModelSerializers(author_data, many=True)
        return Response(bs.data)


# 查找单个作者详细信息
class AuthorsDetailview(APIView):
    # 认证
    authentication_classes = []
    # 解析器
    parser_classes = [JSONParser, FormParser]

    def get(self, request, *args, **kwargs):
        pk=kwargs.get('pk')
        author_data = models.Author.objects.filter(pk=pk).first()
        bs = AuthorsModelSerializers(author_data, many=False)
        return Response(bs.data)


# 根据书的对象查找所有作者
class BookToAuthorview(APIView):
    # 认证
    authentication_classes = []
    # 解析器
    parser_classes = [JSONParser, FormParser]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        book_obj = models.Book.objects.filter(pk=pk).first()
        author_data=book_obj.authors.all()
        bs = AuthorsModelSerializers(author_data, many=True)
        return Response(bs.data)



# 出版社序列化类
class PublishersModelSerializers(serializers.ModelSerializer):
    class Meta:
        model=models.Publish
        fields='__all__'
        depth=1

# 出版社列表
class Publishersview(APIView):
    # 认证
    authentication_classes = []
    # 解析器
    parser_classes = [JSONParser, FormParser]

    def get(self, request, *args, **kwargs):
        publish_data = models.Publish.objects.all()
        bs = PublishersModelSerializers(publish_data, many=True)
        return Response(bs.data)


# 单个出版社信息
class PublishersDetailview(APIView):
    # 认证
    authentication_classes = []
    # 解析器
    parser_classes = [JSONParser, FormParser]

    def get(self, request, *args, **kwargs):
        pk=kwargs.get('pk')
        publish_data = models.Publish.objects.filter(pk=pk).first()
        bs = PublishersModelSerializers(publish_data, many=False)
        return Response(bs.data)