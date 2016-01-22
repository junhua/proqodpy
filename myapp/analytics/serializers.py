from rest_framework import serializers
from django.contrib.auth import get_user_model
from myapp.courses.models import Course
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


# class SubmissionGradeReportSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = SubmissionGradeReport
#         fields = (
#             'id',
#             'submission_id',
#             'submission_type',
#             'grade',

#         )


# class QuestionGradeReportSerializer(serializers.ModelSerializer):
#     submission_grade_report_set = SubmissionGradeReportSerializer(
#         many=True,
#         read_only=True,
#     )

#     class Meta:
#         model = QuestionGradeReport
#         fields = (
#             'id',
#             'question_id',
#             'question_type',
#             'grade',
#             'submission_grade_report_set'

#         )


# class AssessmentGradeReportSerializer(serializers.ModelSerializer):
#     question_grade_report_set = QuestionGradeReportSerializer(
#         many=True,
#         read_only=True
#     )

#     class Meta:
#         model = AssessmentGradeReport
#         fields = (
#             'id',
#             'assessment_id',
#             'grade',
#             'question_grade_report_set',
#         )


# class AcademicReportSerializer(serializers.ModelSerializer):

#     """
#     Structure:

#     AcademicReport
#         - student (unique_together with course)
#         - course  (unique_together with student)
#         - grade (bool)
#         - override (decimal - 5 max digits:, 2 decimal places)
#         - assessment_grade_report_set
#             - assessment
#             - grade
#             - override
#             - question_grade_report_set
#                 - question_id (unique_together with question_type)
#                 - question_type (unique_together with question_id)
#                 - grade
#                 - override
#                 - submission_grade_report_set
#                     - submission_id (unique_together with submission_type)
#                     - submission_type (unique_together with submission_id)
#                     - grade
#                     - override
#     """
#     student = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.filter(user_type=0)
#     )

#     course = serializers.PrimaryKeyRelatedField(
#         queryset=Course.objects.all()
#     )

#     assessment_grade_report_set = AssessmentGradeReportSerializer(
#         many=True,
#         read_only=True
#     )

#     class Meta:
#         model = AcademicReport
#         fields = (
#             'id',
#             'student',
#             'course',
#             'grade',
#             'assessment_grade_report_set',
#         )
