# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-24 20:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20160924_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circle',
            name='admins',
            field=models.ManyToManyField(blank=True, related_name='circle_admins', to='api.Foodie'),
        ),
        migrations.AlterField(
            model_name='circle',
            name='master',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='circle_masters', to='api.Foodie'),
        ),
    ]
