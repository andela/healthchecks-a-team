# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-08 07:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20160415_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='often',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='check',
            name='status',
            field=models.CharField(choices=[('up', 'Up'), ('down', 'Down'), ('new', 'New'), ('paused', 'Paused'), ('often', 'Often')], default='new', max_length=6),
        ),
    ]
