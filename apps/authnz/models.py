from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

from django.db import models

# Create your models here.

class Student(models.Model):

    # Fields
    user = models.OneToOneField(User)
    student_id = models.CharField(max_length=55, primary_key=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.user.username


class Department(models.Model):

    # Fields
    department_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Teacher(models.Model):

    user = models.OneToOneField(User)
    # Setting as one to many first. It should be many to many
    departments = models.ForeignKey('Department', related_name='teachers')

    def __str__(self):
        return self.user.username

class TeachingAssistant(models.Model):

    user = models.OneToOneField(User)
    # Setting as one to many first. It should be many to many
    departments = models.ForeignKey('Department', related_name='TA')

    def __str__(self):
        return self.user.username