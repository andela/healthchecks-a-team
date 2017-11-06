# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-01 09:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20171101_0333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='day_reports_allowed',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='month_reports_allowed',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='week_reports_allowed',
        ),
        migrations.AddField(
            model_name='profile',
            name='days',
            field=models.IntegerField(default=30),
        ),
    ]
