from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import ArrayField
from myapp.courses.models import Question

class PerformanceReport(models.Model):

    """
    Performance report Model for programming specific measurement.
    Fields: complexity, memory, time(Micro-second), size(byte), correctness
    Fields that are under development will return -1 value
    """

    complexity = models.DecimalField(
        _("complexity_index"),
        decimal_places=2,
        max_digits=5,
        null=True,
        blank=True,
        default=0.,
        help_text=_("cyclomatric complexity index"),
    )

    memory = models.DecimalField(
        _("memory_efficiency"),
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True,
        default=0.,
        help_text=_("memory used for the program"),
    )

    time = models.DecimalField(
        _("time_efficiency"),
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True,
        default=0.,
        help_text=_("time used for the program"),
    )

    correctness = models.DecimalField(
        _("correctness_index"),
        decimal_places=2,
        max_digits=5,
        null=True,
        blank=True,
        default=0.,
        help_text=_("correctness index")
    )

    size = models.DecimalField(
        _("file_size"),
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
        default=0.,
        help_text=_("file size")
    )

    # radon raw metrics
    # loc, lloc, sloc, comments, multi, blank
    # radon.metrics.mi_parameters:
    # return the Halstead Volume,
    # the Cyclomatic Complexity
    # the number of LLOC (Logical Lines of Code)
    # the percent of lines of comment

    loc = models.DecimalField(
        _("loc"),
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
        default=0.,
        help_text=_("line of code")
    )

    lloc = models.DecimalField(
        _("lloc"),
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
        default=0.,
        help_text=_("logical line of code")
    )

    sloc = models.DecimalField(
        _("sloc"),
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
        default=0.,
        help_text=_("source lines of code")
    )

    comment_lines = models.DecimalField(
        _("comment_lines"),
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
        default=0.,
        help_text=_("number of lines of comments")
    )

    blank_lines = models.DecimalField(
        _("blank_lines"),
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
        default=0.,
        help_text=_("number of blank lines")
    )

    multi_lines = models.DecimalField(
        _("multi_lines"),
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
        default=0.,
        help_text=_("the number of lines which represent multi-line strings")
    )

    maintainability_index = models.DecimalField(
        _("maintainability_index"),
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
        default=0.,
        help_text=_(
            """
            Maintainability index, Maintainability Index calculates 
            an index value between 0 and 100 that represents the 
            relative ease of maintaining the code. A high value 
            means better maintainability.
            """)
    )

    halstead_volume = models.DecimalField(
        _("halstead_volume"),
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
        default=0.,
        help_text=_(
            """
            Halstead Volume - the size of the implementation of an algorithm. 
            The computation is based on the number of operations performed and 
            operands handled in the algorithm."""
        )
    )

    date_created = models.DateTimeField(
        _('date created'),
        default=timezone.now
    )

    class Meta:
        # abstract = True
        verbose_name = _('performance_report')
        verbose_name_plural = _('performance_reports')
        ordering = ['date_created']

    def __str__(self):
        return str(self.id)

class PeerRankReport(models.Model):

    date_created = models.DateTimeField(
        _('date created'),
        default=timezone.now
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _('peer_rank_report')
        verbose_name_plural = _('peer_rank_reports')
        ordering = ['date_created']


class PeerRank(models.Model):
    PEER_READABLE_RANK = (
        (0, _("Unreadable")),
        (1, _("Fairly readable")),
        (2, _("Mostly readable")),
        (3, _("Highly readable")),
        (4, _("Perfactly readable")),
    )

    PEER_SMART_RANK = (
        (0, _("Poor")),
        (1, _("Normal")),
        (2, _("Cool")),
        (3, _("Brilliant")),
        (4, _("Genius"))
    )

    readability_rank = models.CharField(
        _("readability_rank"),
        max_length=1,
        default=1,
        choices=PEER_READABLE_RANK,
        null=True,
        blank=True,
        help_text=_("peer readability rank")
    )

    smart_rank = models.CharField(
        _("readability_rank"),
        max_length=1,
        default=1,
        choices=PEER_SMART_RANK,
        null=True,
        blank=True,
        help_text=_("peer smart rank")
    )

    report = models.ForeignKey(
        'PeerRankReport',
        related_name="peer_ranks"
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _('peer_rank')
        verbose_name_plural = _('peer_ranks')


class QuestionGradeReport(models.Model):

    TYPE = Question.TYPE

    type = models.PositiveSmallIntegerField(
        _("question type"),
        choices=TYPE
    )

    grade = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    question_id = models.PositiveIntegerField(
        _("question id"),
        null=False,
        blank=False,
        help_text="a question number unique together with the type"
    )

    student = models.ForeignKey(
        "authnz.ProqodUser",
        related_name="grades"
    )
