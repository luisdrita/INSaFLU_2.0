# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-13 17:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('managing_files', '0003_auto_20171212_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaKeyReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='uploaded date')),
                ('value', models.CharField(default='value not needed', max_length=200)),
                ('description', models.TextField(default='')),
                ('meta_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meta_key_reference', to='managing_files.MetaKey')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meta_key_reference', to=settings.AUTH_USER_MODEL)),
                ('reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meta_key_reference', to='managing_files.Reference')),
            ],
            options={
                'ordering': ['reference__id', '-creation_date'],
            },
        ),
    ]
