# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-27 04:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NNModelManager', '0006_nnmodelhistory_current_data_header'),
    ]

    operations = [
        migrations.AddField(
            model_name='nnmodelhistory',
            name='data_rows',
            field=models.IntegerField(default=0),
        ),
    ]