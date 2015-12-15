# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-11 10:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assessment_type', models.CharField(choices=[(0, b'lab'), (1, b'quiz'), (2, b'project'), (3, b'exam')], default=0, max_length=5, verbose_name='assessment type')),
                ('assessment_id', models.PositiveSmallIntegerField(verbose_name='assessment id')),
                ('duration', models.DurationField(null=True, verbose_name='available duration')),
            ],
            options={
                'ordering': ['assessment_type', 'assessment_id'],
                'verbose_name': 'assessment',
                'verbose_name_plural': 'assessments',
            },
        ),
        migrations.CreateModel(
            name='BlankQuestionContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seq', models.PositiveSmallIntegerField(help_text='sequence unique together with question', verbose_name='sequence')),
                ('content', models.CharField(blank=True, max_length=200, verbose_name='content')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_batch', models.CharField(blank=True, help_text='e.g. FY15T3 (for Year 2015 Term 3)', max_length=20, verbose_name='course batch')),
                ('course_code', models.CharField(blank=True, help_text='e.g. CS101', max_length=20, verbose_name='course code')),
                ('school', models.CharField(blank=True, help_text='e.g. SUTD', max_length=100, null=True)),
                ('department', models.CharField(blank=True, help_text='e.g. ISTD', max_length=100, null=True)),
                ('title', models.CharField(blank=True, help_text='e.g. Digital World', max_length=50, null=True)),
                ('description', models.TextField(blank=True, help_text='e.g. An introduction course to programming using Python', max_length=255, null=True)),
                ('programming_language', models.CharField(help_text='e.g. Python', max_length=55, verbose_name='programming language')),
                ('start_date', models.DateField(verbose_name='start date')),
                ('end_date', models.DateField(verbose_name='end date')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created')),
                ('participants', models.ManyToManyField(related_name='courses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_created'],
                'verbose_name': 'course',
                'verbose_name_plural': 'courses',
            },
        ),
        migrations.CreateModel(
            name='MultipleChoices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(blank=True, max_length=200, verbose_name='content')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_num', models.CharField(help_text=b'a question no unique together with the assessment', max_length=10, verbose_name='question no')),
                ('question_type', models.CharField(choices=[(0, b'programming'), (1, b'mcq'), (2, b'blank'), (3, b'others')], default=0, max_length=5, verbose_name='question type')),
                ('title', models.CharField(blank=True, max_length=50, null=True, verbose_name='qustion content')),
                ('question_content', models.TextField(blank=True, null=True, verbose_name='qustion content')),
                ('solution', models.TextField(blank=True, null=True, verbose_name='solution')),
                ('assessment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Assessment')),
            ],
        ),
        migrations.AddField(
            model_name='multiplechoices',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mcq_choices', to='courses.Question'),
        ),
        migrations.AddField(
            model_name='blankquestioncontent',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blank_parts', to='courses.Question'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizes', to='courses.Course'),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set([('course_batch', 'course_code', 'school', 'department')]),
        ),
        migrations.AlterUniqueTogether(
            name='assessment',
            unique_together=set([('assessment_type', 'assessment_id')]),
        ),
    ]
