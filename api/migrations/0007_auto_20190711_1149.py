# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-07-11 11:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='friends',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.UserGroup'),
        ),
        migrations.AddField(
            model_name='friends',
            name='user_type',
            field=models.IntegerField(choices=[(0, '好朋友'), (1, '知心朋友'), (2, '基友'), (3, '生死之交')], default=1),
        ),
    ]
