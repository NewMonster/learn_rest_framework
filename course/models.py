from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType




# Create your models here.
# 普通课程
class Course(models.Model):
    title=models.CharField(max_length=32)
    # 不生成数据库,只用于反向查找
    price_policy_list=GenericRelation('PricePolicy')



# 学位课
class DegreeCourse(models.Model):
    title=models.CharField(max_length=32)
    # 不生成数据库,只用于反向查找
    price_policy_list=GenericRelation('PricePolicy')



# 价格策略
class PricePolicy(models.Model):
    price=models.CharField(max_length=32)
    period=models.CharField(max_length=32)
    # 应用数据库中的content_type表(表中存在所有数据表名称)
    content_type = models.ForeignKey(ContentType,verbose_name='关联的表名')
    object_id = models.IntegerField(verbose_name="关联表的主键")
    # 不生成数据库,帮助快速实现content_type操作
    content_obj=GenericForeignKey('content_type','object_id')



# 自己完成数据的查询
# 给普通课python基础添加价格策略   9.9 一个月
# # 获取课程id
# obj=Course.objects.filter(title='python基础').first()
# # obj.id
# # 获取表名id
# cobj=ContentType.objects.filter(model='course').first()
# # cobj.id
# # 添加数据
# PricePolicy.objects.create(price='9.9',period='一个月',content_type_id=cobj.id,object_id=obj.id)
#

# 使用GenericForeignKey实现
obj=Course.objects.filter(title='python基础').first()
# 自动获取课程和表名id    content_type=obj
PricePolicy.objects.create(price='9.9',period='一个月',content_obj=obj)


