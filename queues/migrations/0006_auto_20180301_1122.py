# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-01 11:22
from __future__ import unicode_literals

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('queues', '0005_auto_20180223_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='subscription',
            field=models.ManyToManyField(blank=True, related_name='subscribers', to='queues.Teacher'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='queue',
            field=models.ManyToManyField(blank=True, related_name='queue', to='queues.Queue'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='subject',
            field=django_mysql.models.ListCharField(models.CharField(max_length=50), blank=True, max_length=765, null=True, size=15),
        ),
    ]
