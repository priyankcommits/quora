# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-04 14:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quorapp', '0017_auto_20160601_0930'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='read',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2016, 6, 4, 14, 54, 27, 525458, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2016, 6, 4, 14, 54, 27, 525738, tzinfo=utc), null=True),
        ),
    ]
