from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField


class Submission(models.Model):
    from myapp.courses.models import Question
    TYPE = Question.TYPE

    id = models.AutoField(primary_key=True)

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
        default=-1.0,
        null=True,
        blank=True,
        help_text=_("100-based overall score")
    )

    type = models.PositiveSmallIntegerField(
        _("type"),
        choices=TYPE,
    )

    class Meta:
        abstract = True
        ordering = ['created_by', 'date_created']


class CodeSubmission(Submission):
    question = models.ForeignKey(
        "courses.ProgrammingQuestion",
        related_name="+"
    )
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

    # def get_score(self):
    #     score = None
    #     code = self.code
    #     unittest_set = self.question.unittests
    #     correct, total = 0.0, len(unittest_set)

    #     for unittest in unittest_set:
    #         correct+=unittest.run.get('pass')
    #     return score


class BlanksSubmission(Submission):
    question = models.ForeignKey(
        "courses.BlankQuestion",
        related_name="+"
    )
    blanks = ArrayField(
        models.CharField(
            max_length=255,
            blank=True,
            null=True
        )
    )


class McqSubmission(Submission):
    question = models.ForeignKey(
        "courses.Mcq",
        related_name="+"
    )
    answer = models.CharField(
        _("choice"),
        max_length=50,
        null=True,
        blank=True,
    )


class CheckoffSubmission(Submission):
    question = models.ForeignKey(
        "courses.CheckoffQuestion",
        related_name="+"
    )
    checked = models.BooleanField(
        _("checked"),
        default=False,
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
    question = models.OneToOneField(
        "courses.ProgrammingQuestion",
        related_name="+"
    )


class BlankQuestionProgress(Progress):
    answer_last_saved = ArrayField(
        models.CharField(
            max_length=255,
            blank=True,
            null=True,
        )
    )
    question = models.OneToOneField(
        "courses.BlankQuestion",
        related_name="+"
    )


class McqProgress(Progress):
    choice = models.OneToOneField(
        "courses.MultipleChoice",
        max_length=50,
        null=True,
        blank=True,
    )
    question = models.OneToOneField(
        "courses.Mcq",
        related_name="+"
    )
