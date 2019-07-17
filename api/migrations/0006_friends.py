# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-07-11 11:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20190711_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('phone', models.CharField(max_length=11, null=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('age', models.IntegerField(null=True)),
                ('school', models.CharField(max_length=100, null=True)),
                ('password', models.CharField(max_length=200)),
            ],
        ),
    ]
