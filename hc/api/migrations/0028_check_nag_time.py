# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-06 14:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_check_nag_interval'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='nag_time',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]
