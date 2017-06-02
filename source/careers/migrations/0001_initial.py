# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-29 21:45
from __future__ import unicode_literals

import careers.models
import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Career',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=careers.models.upload_location, width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('entry', models.CharField(max_length=120)),
                ('experience', ckeditor_uploader.fields.RichTextUploadingField()),
                ('education', ckeditor_uploader.fields.RichTextUploadingField()),
                ('draft', models.BooleanField(default=False)),
                ('publish', models.DateField()),
                ('updated', models.DateField(auto_now=True)),
                ('timestamp', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(unique=True)),
                ('overview', models.TextField()),
                ('updated', models.DateField(auto_now=True)),
                ('timestamp', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='career',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='careers.Category'),
        ),
        migrations.AddField(
            model_name='career',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
