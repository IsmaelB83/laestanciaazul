# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-26 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20171226_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='author',
            field=models.BooleanField(default=False),
        ),
    ]
