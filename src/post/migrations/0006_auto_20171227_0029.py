# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-26 23:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_remove_postarchive_category'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='postarchive',
            unique_together=set([('year', 'month')]),
        ),
    ]