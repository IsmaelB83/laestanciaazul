# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-30 18:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loguser',
            old_name='text',
            new_name='description',
        ),
    ]