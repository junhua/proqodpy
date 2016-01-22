from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import ArrayField


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
        help_text=_("Halstead Volume")
    )

    date_created = models.DateTimeField(
        _('date created'),
        default=timezone.now
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        # abstract = True
        verbose_name = _('performance_report')
        verbose_name_plural = _('performance_reports')
        ordering = ['date_created']


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


class Grade(models.Model):

    grade = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class QuestionGrade(Grade):
    pass

    # class SubmissionGradeReport(models.Model):

    #     grade = models.DecimalField(
    #         _("grade"),
    #         max_digits=5,
    #         decimal_places=2,
    #         null=True,
    #         blank=True
    #     )

    #     class Meta:
    #         abstract = True

    # class GradeReport(models.Model):
    #     grade = models.DecimalField(
    #         _("grade"),
    #         max_digits=5,
    #         decimal_places=2,
    #         null=True,
    #         blank=True
    #     )
    #     dt_created = models.DateTimeField(
    #         _("datetime_created"),
    #         auto_now=True,
    #     )

    #     class Meta:
    #         abstract = True

    # class AcademicReport(GradeReport):

    #     """
    #     Structure:

    #     AcademicReport
    #         - student (unique_together with course)
    #         - course  (unique_together with student)
    #         - grade (decimal)

    #         - assessment_grade_report_set
    #             - assessment
    #             - grade

    #             - question_grade_report_set
    #                 - question_id (unique_together with question_type)
    #                 - question_type (unique_together with question_id)
    #                 - grade

    #                 - submission_grade_report_set
    #                     - submission_id (unique_together with submission_type)
    #                     - submission_type (unique_together with submission_id)
    #                     - grade

    #     """

    #     student = models.OneToOneField(
    #         "authnz.ProqodUser",
    #         related_name='academic_report',
    #     )
    #     course = models.OneToOneField(
    #         "courses.course",
    #         related_name="+"
    #     )

    #     class Meta:
    #         verbose_name = _('academic_report')
    #         unique_together = ('student', 'course',)

    # class AssessmentGradeReport(GradeReport):
    #     academic_report = models.ForeignKey(
    #         "AcademicReport",
    #         related_name="assessment_grade_set"
    #     )
    #     assessment = models.OneToOneField(
    #         "courses.Assessment",
    #         related_name="+"
    #     )

    #     class Meta:
    #         verbose_name = _('assessment_grade_report')

    # class QuestionGradeReport(GradeReport):
    #     from myapp.courses.models import Question
    #     assessment_grade_report = models.ForeignKey(
    #         "AssessmentGradeReport",
    #         related_name="question_grade_set"
    #     )
    #     question_id = models.PositiveIntegerField(
    #         _("question_id"),
    #         null=False,
    #         blank=False,
    #     )
    #     question_type = models.PositiveSmallIntegerField(
    #         _("question_type"),
    #         choices=Question.TYPE,
    #         null=False,
    #         blank=False
    #     )

    #     class Meta:
    #         verbose_name = _('question_grade_report')
    #         unique_together = ('question_id', 'question_type')

    # class SubmissionGradeReport(GradeReport):
    #     from myapp.submissions.models import Submission
    #     TYPE = Submission.TYPE
    #     question_grade_report = models.ForeignKey(
    #         "QuestionGradeReport",
    #         related_name="submission_grade_set"
    #     )
    #     submission_id = models.PositiveIntegerField(
    #         _("submission_id"),
    #         null=False,
    #         blank=False
    #     )
    #     submission_type = models.PositiveSmallIntegerField(
    #         _("submission_type"),
    #         choices=TYPE,
    #         null=False,
    #         blank=False
    #     )

    #     class Meta:
    #         verbose_name = _('submission_grade_report')
    #         unique_together = ('submission_id', 'submission_type')
