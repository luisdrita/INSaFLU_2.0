# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-21 17:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('managing_files', '0005_remove_uploadfiles_is_samples_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadfiles',
            name='is_first_fastq_file',
        ),
    ]
