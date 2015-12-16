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
    question = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = MultipleChoice
        fields = (
            'id',
            'content',
            'question',
        )


class BlankQuestionContentSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = BlankQuestionContent
        fields = (
            'id',
            'seq',
            'content',
            'question',
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
    course = CourseSerializer(read_only=True)
    duration = serializers.DurationField()
    assessment_type = serializers.ChoiceField(
        choices=Assessment.ASSESSMENT_TYPE)
    # mcq_questions = McqQuestionSerializer(many=True)
    # blank_questions = BlankQuestionSerializer(many=True)
    # programming_questions = ProgrammingQuestionSerializer(many=True)
    questions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Assessment
        fields = (
            'id',
            'assessment_type',
            'assessment_id',
            'duration',
            'course',
            'questions'
        )


class McqQuestionSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(read_only=True)
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
    assessment = serializers.PrimaryKeyRelatedField(read_only=True)
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
    assessment = serializers.PrimaryKeyRelatedField(read_only=True)
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
