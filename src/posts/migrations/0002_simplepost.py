# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-19 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('posts', '0001_initial'), ]

    operations = [migrations.CreateModel(name='SimplePost',
        fields=[('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('title', models.CharField(default='none', max_length=120)),
            ('image', models.FileField(upload_to='')), ], ), ]