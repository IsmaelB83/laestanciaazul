# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-26 09:05
from __future__ import unicode_literals

from django.db import migrations, models
import gallery.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='height_field',
        ),
        migrations.RemoveField(
            model_name='image',
            name='width_field',
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=gallery.models.upload_location_postimage),
        ),
    ]