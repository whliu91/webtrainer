# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-07-16 10:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NNModelManager', '0015_auto_20180716_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nnmodelhistory',
            name='weights_json',
            field=models.CharField(blank=True, default=None, max_length=5000, null=True),
        ),
    ]
