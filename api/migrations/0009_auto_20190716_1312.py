# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-07-16 13:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_friends_roles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='roles',
            field=models.ManyToManyField(to='api.Roles'),
        ),
    ]
