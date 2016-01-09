from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *
from myapp.courses.models import *
from myapp.analytics.serializers import PerformanceReportSerializer

User = get_user_model()


class CodeSubmissionSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    question = serializers.PrimaryKeyRelatedField(
        queryset=ProgrammingQuestion.objects.all()
    )
    score = serializers.DecimalField(
        max_digits=5, decimal_places=2, read_only=True
    )
    performance_report = PerformanceReportSerializer(
        read_only=True
    )
    type = serializers.IntegerField(
        default=Question.PROGRAMMING, read_only=True)

    class Meta:
        model = CodeSubmission
        fields = (
            'id',
            'type',
            'code',
            'created_by',
            'question',
            'date_created',
            # 'score',
            'performance_report',
        )


class BlanksSubmissionSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    question = serializers.PrimaryKeyRelatedField(
        queryset=BlankQuestion.objects.all()
    )
    blanks = serializers.ListField(
        child=serializers.CharField(max_length=255)
    )
    type = serializers.IntegerField(
        default=Question.BLANKS, read_only=True)

    class Meta:
        model = BlanksSubmission
        fields = (
            'id',
            'type',
            'blanks',
            'created_by',
            'question',
            'date_created',
            # 'score',
        )


class McqSubmissionSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    question = serializers.PrimaryKeyRelatedField(
        queryset=Mcq.objects.all()
    )
    type = serializers.IntegerField(
        default=Question.MCQ, read_only=True)

    class Meta:
        model = McqSubmission
        fields = (
            'id',
            'type',
            'answer',
            'created_by',
            'question',
            'date_created',
            # 'score',
        )


class CheckoffSubmissionSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    question = serializers.PrimaryKeyRelatedField(
        queryset=CheckoffQuestion.objects.all()
    )
    type = serializers.IntegerField(
        default=Question.CHECKOFF, read_only=True)

    class Meta:
        model = CheckoffSubmission
        fields = (
            'id',
            'type',
            'created_by',
            'question',
            'date_created',
            'score',
            'checked',
        )


class ProgrammingQuestionProgressSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(user_type=0)
    )
    question = serializers.PrimaryKeyRelatedField(
        queryset=ProgrammingQuestion.objects.all()
    )

    class Meta:
        model = ProgrammingQuestionProgress
        fields = (
            'id',
            'student',
            'question',
            'answer_last_saved',
            'date_last_updated',
        )
        read_only_fields = ('status',)


class BlankQuestionProgressSerializer(serializers.ModelSerializer):
    answer_last_saved = serializers.ListField(
        child=serializers.CharField(max_length=255)
    )
    student = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(user_type=0)
    )
    question = serializers.PrimaryKeyRelatedField(
        queryset=BlankQuestion.objects.all()
    )

    class Meta:
        model = BlankQuestionProgress
        fields = (
            'id',
            'student',
            'question',
            'answer_last_saved',
            'date_last_updated',
        )
        read_only_fields = ('status',)


class McqProgressSerializer(serializers.ModelSerializer):

    student = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(user_type=0)
    )
    question = serializers.PrimaryKeyRelatedField(
        queryset=Mcq.objects.all()
    )
    choice = serializers.PrimaryKeyRelatedField(
        queryset=MultipleChoice.objects.all()
    )

    class Meta:
        model = McqProgress
        fields = (
            'id',
            'student',
            'question',
            'choice',
            'date_last_updated',
        )
        read_only_fields = ('status',)
