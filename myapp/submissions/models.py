from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField


class Submission(models.Model):

    id = models.AutoField(primary_key=True)

    question = models.ForeignKey(
        "courses.Question",
        related_name="+"
    )

    date_created = models.DateTimeField(
        _('date created'),
        default=timezone.now,
        editable=False,
    )

    created_by = models.ForeignKey(
        "authnz.ProqodUser",
        related_name="+",
        unique=False
    )

    score = models.DecimalField(
        _("oversall_score"),
        decimal_places=2,
        max_digits=5,
        null=True,
        blank=True,
        help_text=_("100-based overall score")
    )

    class Meta:
        abstract = True
        ordering = ['created_by', 'date_created']


class CodeSubmission(Submission):
    code = models.TextField(
        _("code"),
        blank=True,
        null=True,
    )

    performance_report = models.OneToOneField(
        'analytics.PerformanceReport',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )


class BlanksSubmission(Submission):
    blanks = ArrayField(
        models.CharField(
            max_length=255,
            blank=True,
            null=True
        )
    )


class McqSubmission(Submission):
    answer = models.CharField(
        _("choice"),
        max_length=50,
        null=True,
        blank=True,
    )


class Progress(models.Model):

    NO_RECORD, WRONG, COMPLETE = range(3)
    STATUS = (
        (NO_RECORD, 'no record'),
        (WRONG, 'wrong'),
        (COMPLETE, 'complete'),
    )
    """
    Models to store student's progress for each question.
    Student and Question is unique_together
    """
    student = models.OneToOneField(
        "authnz.ProqodUser",
        related_name="+"
    )
    question = models.OneToOneField(
        "courses.Question",
        related_name="+"
    )

    status = models.PositiveSmallIntegerField(
        _("status"),
        default=NO_RECORD,
        choices=STATUS,
        help_text=_(
            "Status of the question - 0: NO_RECORD; 1: WRONG; 2: COMPLETE;"
        )
    )

    date_last_updated = models.DateTimeField(
        _("last_update"),
        auto_now=True,
    )

    class Meta:
        unique_together = ('student', 'question')
        abstract = True


class ProgrammingQuestionProgress(Progress):
    answer_last_saved = models.TextField(
        _("answer_last_saved"),
        null=True,
        blank=True,
    )


class BlankQuestionProgress(Progress):
    answer_last_saved = ArrayField(
        models.CharField(
            max_length=255,
            blank=True,
            null=True,
        )
    )


class McqProgress(Progress):
    answer_last_saved = models.CharField(
        _("choice"),
        max_length=50,
        null=True,
        blank=True,
    )
