from django.shortcuts import render
from course import models
from django.http.response import HttpResponse

# Create your views here.
def test(request):
    # 给普通课python基础添加价格策略   9.9 一个月
    # # 使用GenericForeignKey实现
    # obj = models.Course.objects.filter(title='python基础').first()
    # # 自动获取课程和表名id    content_type=obj
    # models.PricePolicy.objects.create(price='9.9', period='一个月', content_obj=obj)
    #
    # # 使用GenericForeignKey实现
    # obj = models.Course.objects.filter(title='python基础').first()
    # # 自动获取课程和表名id    content_type=obj
    # models.PricePolicy.objects.create(price='19.9', period='两个月', content_obj=obj)
    #
    # # 使用GenericForeignKey实现
    # obj = models.Course.objects.filter(title='python基础').first()
    # # 自动获取课程和表名id    content_type=obj
    # models.PricePolicy.objects.create(price='29.9', period='三个月', content_obj=obj)




    # # 使用GenericForeignKey实现
    # obj = models.DegreeCourse.objects.filter(title='python数据分析').first()
    # # 自动获取课程和表名id    content_type=obj
    # models.PricePolicy.objects.create(price='9.9', period='一个月', content_obj=obj)
    #
    # # 使用GenericForeignKey实现
    # obj = models.DegreeCourse.objects.filter(title='python数据分析').first()
    # # 自动获取课程和表名id    content_type=obj
    # models.PricePolicy.objects.create(price='19.9', period='两个月', content_obj=obj)
    #
    # # 使用GenericForeignKey实现
    # obj = models.DegreeCourse.objects.filter(title='python数据分析').first()
    # # 自动获取课程和表名id    content_type=obj
    # models.PricePolicy.objects.create(price='29.9', period='三个月', content_obj=obj)

    # 根据课程id获取全部的所有价格策略
    course=models.DegreeCourse.objects.filter(id=1).first()
    policys=course.price_policy_list.all()

    print(policys)

    return HttpResponse("添加成功")