# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-31 12:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_profile_current_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='daily_reports_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='monthly_reports_allowed',
            field=models.BooleanField(default=False),
        ),
    ]
