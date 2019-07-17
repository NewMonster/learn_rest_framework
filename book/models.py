from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=32)
    price = models.IntegerField()
    pub_date = models.DateField()
    publish = models.ForeignKey("Publish")
    authors = models.ManyToManyField("Author")

    def __str__(self):
        return self.title


class Publish(models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField()


    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()

    def __str__(self):
        return self.name

from datetime import datetime



class Users(models.Model):
    USER_TYPE = (
        (0,'无效用户'),
        (1, '普通用户'),
        (2, 'VIP'),
        (3, 'SVIP')
    )
    name=models.CharField(max_length=32)
    age=models.IntegerField()
    rdate=models.DateField(default=datetime.date(datetime.now()))
    password = models.CharField(max_length=64)
    user_type = models.IntegerField(choices=USER_TYPE, default=1)

    def __str__(self):
        return self.name

    # class Meta:
    #     db_table='user'
    #     verbose_name='用户'
    #     verbose_name_plural='用户组'

class UserToken(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)

    def __str__(self):
        return self.user.name

    # class Meta:
    #     db_table='token'
    #     verbose_name='token'
    #     verbose_name_plural='token组'




