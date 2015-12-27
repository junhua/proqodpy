from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import (
    CodeSubmission,
    BlanksSubmission,
    McqSubmission,
)
from myapp.courses.models import (
    Question,
)
User = get_user_model()


class CodeSubmissionSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all()
    )

    class Meta:
        model = CodeSubmission
        fields = (
            'id',
            'code',
            'created_by',
            'question',
        )
        readonly_fields = (
            'date_created',
            'score',
            'performance_report',
        )


class BlanksSubmissionSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all()
    )
    blanks = serializers.ListField(
        child=serializers.CharField(max_length=255)
    )

    class Meta:
        model = BlanksSubmission
        fields = (
            'id',
            'blanks',
            'created_by',
            'question',

        )

        readonly_fields = (
            'date_created',
            'score',
        )


class McqSubmissionSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all()
    )

    class Meta:
        model = McqSubmission
        fields = (
            'id',
            'answer',
            'created_by',
            'question',
        )
        readonly_fields = (
            'date_created',
            'score',
        )
