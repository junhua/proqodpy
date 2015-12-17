from rest_framework import serializers
from .models import (
    Course,
    Assessment,
    Question,
    MultipleChoice,
    BlankQuestionContent
)
from authnz.models import ProqodUser


class MultipleChoiceSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        # queryset=Question.objects.all()
        read_only=True
    )

    class Meta:
        model = MultipleChoice
        fields = (
            'id',
            'content',
            'question',
            'is_correct',
        )


class BlankQuestionContentSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all()
    )

    class Meta:
        model = BlankQuestionContent
        fields = (
            'id',
            'part_seq',
            'content',
            'question',
        )

    def __str__(self):
        return "Q%s Number %s" % (self.question, self.seq)


class McqQuestionSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(
        queryset=Assessment.objects.all()
    )
    question_type = serializers.HiddenField(default=Question.MCQ)

    class Meta:
        model = Question
        fields = (
            'id',
            'assessment',
            'question_num',
            'question_type',
            'title',
            'question_content',
            'solution',
        )


class BlankQuestionSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(
        queryset=Assessment.objects.all()
    )
    question_type = serializers.HiddenField(default=Question.BLANKS)
    blank_parts = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'assessment',
            'question_num',
            'question_type',
            'title',
            'question_content',
            'solution',
            'blank_parts',
        )


class ProgrammingQuestionSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(
        queryset=Assessment.objects.all()
    )
    question_type = serializers.HiddenField(default=Question.PROGRAMMING)

    class Meta:
        model = Question
        fields = (
            'id',
            'assessment',
            'question_num',
            'question_type',
            'title',
            'question_content',
            'solution',
        )


class CourseSerializer(serializers.ModelSerializer):

    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ProqodUser.objects.order_by('id')
    )

    class Meta:
        model = Course
        fields = (
            'id',
            'course_batch',
            'course_code',
            'school',
            'department',
            'title',
            'description',
            'programming_language',
            'start_date',
            'end_date',
            'participants',
        )
        search_fields = ('school', )
        ordering_fields = ('school', 'department', 'id', )


class AssessmentSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all()
    )

    assessment_type = serializers.ChoiceField(
        choices=Assessment.ASSESSMENT_TYPE
    )

    class Meta:
        model = Assessment
        fields = (
            'id',
            'assessment_type',
            'assessment_id',
            'start_date',
            'end_date',
            'course',
        )
