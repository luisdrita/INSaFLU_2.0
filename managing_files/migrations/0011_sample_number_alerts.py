# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-07 12:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managing_files', '0010_auto_20180103_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='number_alerts',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
