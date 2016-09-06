# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-02 05:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20160902_0326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')], default='open', max_length=120)),
                ('Restaurant', models.ManyToManyField(to='api.Restaurant')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Foodie')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Restaurant')),
                ('foodie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Foodie')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Poll')),
            ],
        ),
    ]