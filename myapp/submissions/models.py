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


class UnittestEntry(models.Model):

    visibility = models.BooleanField(
        _('visibility'),
        default=True
    )

    actual_output = models.CharField(
        _("actual_output"),
        null=True,
        blank=True,
        max_length=1024
    )
    is_correct = models.BooleanField(
        _("is_correct"),
    )

    inputs = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    expected_output = models.CharField(
        _("expected_output"),
        null=True,
        blank=True,
        max_length=1024
    )

    subm = models.ForeignKey(
        "CodeSubmission",
        null=True,
        related_name="unittest_entries"
    )

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name_plural = _('unittest_entries')


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

    def get_grade(self):
        assert self.performance_report.correctness is not None
        return max(0., self.performance_report.correctness)


class BlankSubmission(Submission):
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

    evaluation = ArrayField(
        models.BooleanField(),
        blank=True,
        null=True,
        help_text=_("list of blank evaluation")
    )

    def get_grade(self):
        assert type(self.evaluation) is list
        assert len(self.evaluation) > 0
        assert type(self.evaluation[0]) is bool

        return round((sum(self.evaluation) + 0.) / len(self.evaluation), 2)


class McqSubmission(Submission):
    question = models.ForeignKey(
        "courses.Mcq",
        related_name="+"
    )

    answer = models.OneToOneField(
        "courses.MultipleChoice",
        related_name="+"
    )

    def get_grade(self):
        assert self.answer.is_correct is not None
        assert type(self.answer.is_correct) is bool

        return int(self.answer.is_correct)


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

    student = models.ForeignKey(
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
        # unique_together = ('student', 'question')
        abstract = True


class ProgrammingQuestionProgress(Progress):
    answer_last_saved = models.TextField(
        _("answer_last_saved"),
        null=True,
        blank=True,
    )
    question = models.ForeignKey(
        "courses.ProgrammingQuestion",
    )


class BlankQuestionProgress(Progress):
    answer_last_saved = ArrayField(
        models.CharField(
            max_length=255,
            blank=True,
            null=True,
        )
    )
    question = models.ForeignKey(
        "courses.BlankQuestion",
    )


class McqProgress(Progress):
    choice = models.ForeignKey(
        "courses.MultipleChoice",
        max_length=50,
        null=True,
        blank=True,
    )
    question = models.ForeignKey(
        "courses.Mcq",
    )
