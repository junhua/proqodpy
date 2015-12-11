from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
# Create your models here.

class CourseManager(models.Manager):
    pass

class Course(models.Model):

    # Unique-together fields
    course_batch = models.CharField(_('course batch'), max_length=20, blank=True, null=False, 
                                    help_text=_('e.g. FY15T3 (for Year 2015 Term 3)')) # e.g. FY15T3
    course_code = models.CharField(_('course code'), max_length=20, blank=True, null=False, 
                                    help_text=_('e.g. CS101')) # e.g. CS101
    school = models.CharField(max_length=100, blank=True, null=True, help_text=_('e.g. SUTD')) # e.g. SUTD
    department = models.CharField(max_length=100, blank=True, null=True, help_text=_('e.g. ISTD')) # e.g. ISTD
    
    # Other fields
    title = models.CharField(max_length=50, blank=True, null=True, help_text=_('e.g. Digital World')) # e.g. Introduction to programming
    description = models.TextField(max_length=255, blank=True, null=True, 
                                    help_text=_('e.g. An introduction course to programming using Python')) # e.g. An introduction course to programming using Python
    programming_language = models.CharField(_('programming language'), max_length=55, blank=False, null=False, help_text=_('e.g. Python')) # e.g. Python
    start_date = models.DateField(_('start date'), null=False, blank=False) # 1/30/16
    end_date = models.DateField(_('end date'), null=False, blank=False) # 4/30/16
    date_created = models.DateTimeField(_('date created'), default=timezone.now)

    # Foreign keys
    participants = models.ManyToManyField('authnz.ProqodUser', related_name='courses')
    

    objects = CourseManager()

    class Meta:
        verbose_name=_('course')
        verbose_name_plural=_('courses')
        ordering = ['date_created']
        unique_together=("course_batch", "course_code", "school", "department")

    def get_absolute_path(self):
    	return "/courses/%i/" % self.pk

    def __str__(self):
        return "%s_%s_%s_%s"%(school, department, courseCode, title)