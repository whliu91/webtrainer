# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-07-08 03:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NNModelManager', '0010_auto_20180706_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nnmodelhistory',
            name='data_file_path',
            field=models.FilePathField(blank=True, default=None, null=True, path='/home/weihang/Documents/projects/webtrainer/src/com/django/django/webtrainer/uploads/data'),
        ),
    ]
