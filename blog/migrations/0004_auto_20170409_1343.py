# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-09 11:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20170409_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='db_database_name',
            field=models.CharField(blank='true', max_length=200),
        ),
        migrations.AddField(
            model_name='file',
            name='db_port',
            field=models.CharField(blank='true', max_length=200),
        ),
    ]