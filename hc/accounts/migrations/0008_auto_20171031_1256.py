# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-31 12:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20171031_1237'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='monthly_reports_allowed',
            new_name='weekly_reports_allowed',
        ),
    ]
