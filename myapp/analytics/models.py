from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
# from django.utils import timezone
from django.db import models


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


class PerformanceReport(models.Model):

    """ Report Model """

    complexity = models.DecimalField(
        _("complexity_index"),
        decimal_places=2,
        max_digits=5,
        null=True,
        blank=True,
        help_text=_("complexity index, the higher the more complex"),
    )

    memory = models.DecimalField(
        _("memory_efficiency"),
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True,
        help_text=_("memory used for the program"),
    )

    time = models.DecimalField(
        _("time_efficiency"),
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True,
        help_text=_("time used for the program"),
    )

    correctness = models.DecimalField(
        _("correctness_index"),
        decimal_places=2,
        max_digits=5,
        null=True,
        blank=True,
        help_text=_("correctness index")
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        # abstract = True
        verbose_name = _('performance_report')
        verbose_name_plural = _('performance_reports')


class PeerRankReport(models.Model):

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _('peer_rank_report')
        verbose_name_plural = _('peer_rank_reports')


class PeerRank(models.Model):

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
