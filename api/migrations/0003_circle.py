# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-24 18:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20160914_0409'),
    ]

    operations = [
        migrations.CreateModel(
            name='Circle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('street', models.CharField(max_length=120)),
                ('city', models.CharField(max_length=120)),
                ('state', models.CharField(max_length=120)),
                ('lat', models.DecimalField(decimal_places=10, max_digits=12)),
                ('log', models.DecimalField(decimal_places=10, max_digits=12)),
                ('foodies', models.ManyToManyField(to='api.Foodie')),
            ],
        ),
    ]
