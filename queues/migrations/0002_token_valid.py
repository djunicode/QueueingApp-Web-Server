# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-10 08:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queues', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='valid',
            field=models.BooleanField(default=False),
        ),
    ]