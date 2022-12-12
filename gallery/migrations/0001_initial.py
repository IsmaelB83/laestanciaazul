# Generated by Django 4.1.4 on 2022-12-10 10:14

from django.db import migrations, models
import gallery.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(blank=True, default='No caption', max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('post_slug', models.SlugField(max_length=120)),
                ('show_gallery', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to=gallery.models.upload_location_postimage)),
            ],
        ),
    ]
