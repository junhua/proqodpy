# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-08 08:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authnz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proqoduser',
            name='sid',
            field=models.CharField(max_length=55, unique=True, verbose_name='sid'),
        ),
    ]
