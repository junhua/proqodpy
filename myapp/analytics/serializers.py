from rest_framework import serializers
from django.contrib.auth import get_user_model
# from myapp.courses.models import Course
from .models import *

User = get_user_model()


class PerformanceReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = PerformanceReport
        fields = (
            'complexity',
            'time',
            'memory',
            'correctness',
            'size',
            'halstead_volume',
            'lloc',
            'loc',
            'sloc',
            'comment_lines',
            'blank_lines',
            'multi_lines',
            'maintainability_index',
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


# class GradeReportEntrySerializer(serializers.ModelSerializer):

#     class Meta:
#         model = GradeReportEntry
#         fields = (
#             'id',
#             'week',
#             'assessment',
#             'question',
#             'report',
#             'grade',
#             'total'
#         )


# class GradeReportSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = GradeReport
#         fields = (
#             'student',
#             'entries',
#             'grade',
#             'total'
            
#         )
