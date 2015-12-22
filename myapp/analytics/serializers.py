from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    PerformanceReport,
    PeerRankReport,
    PeerRank,
)

User = get_user_model()


class PerformanceReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = PerformanceReport
        fields = (
            'complexity',
            'time',
            'memory',
            'correctness',
        )


class PeerRankSerializer(serializers.ModelSerializer):
    report = serializers.PrimaryKeyRelatedField(
        queryset=PeerRankReport.objects.all()
    )

    class Meta:
        model = PeerRank
        fields = (
            'readability_rank',
            'smart_rank',
            'report',
        )


class PeerRankReportSerializer(serializers.ModelSerializer):
    peer_ranks = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = PeerRankReport
        fields = (
            'id',
            'peer_ranks',
        )
