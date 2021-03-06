# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-01 09:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quorapp', '0016_auto_20160601_0920'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('quorapp.post',),
        ),
        migrations.AddField(
            model_name='post',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quorapp.Answer'),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2016, 6, 1, 9, 30, 18, 255785, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2016, 6, 1, 9, 30, 18, 256155, tzinfo=utc), null=True),
        ),
    ]
