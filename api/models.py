from django.db import models




class UserGroup(models.Model):
    title=models.CharField(max_length=32)




# Create your models here.
class Users(models.Model):
    USER_TYPE = [
        (0, "无效用户"),
        (1, "普通用户"),
        (2, "vip"),
        (3, "svip"),
    ]
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    user_type=models.IntegerField(choices=USER_TYPE,default=1)
    group=models.ForeignKey("UserGroup",null=True)
    roles=models.ManyToManyField("Roles")




class UserToken(models.Model):
    user=models.OneToOneField(to='Users')
    token=models.CharField(max_length=200,unique=True)




class Roles(models.Model):
    title=models.CharField(max_length=32)
    




class Friends(models.Model):
    TYPE = [
        (0, "好朋友"),
        (1, "知心朋友"),
        (2, "基友"),
        (3, "生死之交"),
    ]
    name=models.CharField(max_length=32,unique=True)
    phone=models.CharField(max_length=11,null=True)
    email=models.EmailField(max_length=100,unique=True)
    age=models.IntegerField(null=True)
    school=models.CharField(max_length=100,null=True)
    password=models.CharField(max_length=200)
    group=models.ForeignKey('UserGroup',default=1)
    user_type = models.IntegerField(choices=TYPE, default=1)
    roles=models.ManyToManyField("Roles",default=1)


    def get_friends_info(self):
        roles_object_list=self.roles.all()
        ret=[]
        for item in roles_object_list:
            ret.append({'id':item.id,"title":item.title})
        return ret




