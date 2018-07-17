# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-20 05:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NNModelManager', '0003_nnmodelhistory_num_neurons_layer_str'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nnmodelhistory',
            name='data_file',
            field=models.FileField(blank=True, default=None, null=True, upload_to='uploads/data/'),
        ),
        migrations.AlterField(
            model_name='nnmodelhistory',
            name='min_train_err',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='nnmodelhistory',
            name='weights_json',
            field=models.CharField(blank=True, default=None, max_length=500, null=True),
        ),
    ]