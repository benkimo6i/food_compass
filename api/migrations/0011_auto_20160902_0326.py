# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-02 03:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20160902_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='added',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 9, 2, 3, 26, 50, 771072, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 9, 2, 3, 26, 57, 123400, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
