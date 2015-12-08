from django.db import models

# Create your models here.

class Course(models.Model):

    # Fields

    courseCode = models.CharField(max_length=32, blank=True, null=False, unique=True) # e.g. CS101
    title = models.CharField(max_length=128, blank=True, null=True) # e.g. Introduction to programming
    school = models.CharField(max_length=128, blank=True, null=True) # e.g. SUTD
    department = models.CharField(max_length=128, blank=True, null=True) # e.g. ISTD
    description = models.TextField(max_length=255, blank=True, null=True) # e.g. An introduction course to programming using Python
    programming_language = models.CharField(max_length=55, blank=True, null=False) # e.g. Python
    startDate = models.DateField(null=False, blank=False) # 1/30/16
    endDate = models.DateField(null=False, blank=False) # 4/30/16

    # teachers = models.ManyToManyField('authnz.Teacher', blank=True, null=False)
    # teachingAssistants = models.ManyToManyField('authnz.Assistant', blank=True, null=True)
    # students = models.ManyToManyField('authnz.Student', blank=True, null=False)

    # objects = managers.CourseManager()

    def get_absolute_path(self):
    	return "/courses/%i/" % self.pk

    def __str__(self):
        return "%s_%s_%s_%s"%(school, department, courseCode, title)