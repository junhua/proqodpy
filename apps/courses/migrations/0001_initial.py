# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('courseCode', models.CharField(unique=True, max_length=32, blank=True)),
                ('title', models.CharField(max_length=128, null=True, blank=True)),
                ('school', models.CharField(max_length=128, null=True, blank=True)),
                ('department', models.CharField(max_length=128, null=True, blank=True)),
                ('description', models.TextField(max_length=255, null=True, blank=True)),
                ('programming_language', models.CharField(max_length=55, blank=True)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
            ],
        ),
    ]
