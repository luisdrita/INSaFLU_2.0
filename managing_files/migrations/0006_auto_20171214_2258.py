# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-14 22:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('managing_files', '0005_auto_20171214_1403'),
    ]

    operations = [
        migrations.RenameField(
            model_name='countvariations',
            old_name='var_bigger_50',
            new_name='var_bigger_50_90',
        ),
        migrations.RemoveField(
            model_name='countvariations',
            name='project_sample',
        ),
        migrations.AddField(
            model_name='countvariations',
            name='var_bigger_90',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='projectsample',
            name='count_variations',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_sample', to='managing_files.CountVariations'),
        ),
    ]
