# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-21 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managing_files', '0003_auto_20171221_1132'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sample',
            old_name='is_rejected',
            new_name='is_deleted',
        ),
        migrations.AddField(
            model_name='sample',
            name='candidate_file_name_1',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='candidate_file_name_2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='file_name_1',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='file_name_2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
