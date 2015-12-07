from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

from django.db import models

# Create your models here.

class Student(models.Model):
    # Fields
    user = models.OneToOneField(User)
    student_id = models.CharField(max_length=55, null=True, blank=True)
    school = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):              # __unicode__ on Python 2
        return self.user.username

class Teacher(models.Model):
    # Fields
    user = models.OneToOneField(User)
    teacher_id = models.CharField(max_length=55, null=True, blank=True)
    school = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):              # __unicode__ on Python 2
        return self.user.username

class TeachingAssistant(models.Model):
    # Fields
    user = models.OneToOneField(User)
    ta_id = models.CharField(max_length=55, null=True, blank=True)
    school = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):              # __unicode__ on Python 2
        return self.user.username
