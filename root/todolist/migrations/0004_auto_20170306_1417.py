# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-06 13:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0003_auto_20170223_1143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='date',
        ),
        migrations.AddField(
            model_name='task',
            name='archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]