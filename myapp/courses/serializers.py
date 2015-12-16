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
        queryset=Question.objects.all())

    class Meta:
        model = MultipleChoice
        fields = (
            'id',
            'content',
            'question',
        )


class BlankQuestionContentSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all())

    class Meta:
        model = BlankQuestionContent
        fields = (
            'id',
            'seq',
            'content',
            'question',
        )


class McqQuestionSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(
        queryset=Assessment.objects.all())
    question_type = serializers.HiddenField(default=Question.MCQ)
    choices = MultipleChoiceSerializer(many=True)

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
            'choices',
        )


class BlankQuestionSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(
        queryset=Assessment.objects.all())
    question_type = serializers.HiddenField(default=Question.BLANKS)
    blank_content = serializers.StringRelatedField(many=True, read_only=True)

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
            'blank_content',
        )


class ProgrammingQuestionSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(
        queryset=Assessment.objects.all())
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
    # course = serializers.StringRelatedField(queryset=Course.objects.all())

    assessment_type = serializers.ChoiceField(
        choices=Assessment.ASSESSMENT_TYPE)

    mcq_questions = serializers.StringRelatedField(many=True)

    blank_questions = serializers.StringRelatedField(many=True)

    programming_questions = serializers.StringRelatedField(many=True)

    class Meta:
        model = Assessment
        fields = (
            'id',
            'assessment_type',
            'assessment_id',
            'start_date',
            'end_date',
            'course',
            'mcq_questions',
            'blank_questions',
            'programming_questions',
        )
