from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *

User = get_user_model()


class MultipleChoiceSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=Mcq.objects.all()
    )

    class Meta:
        model = MultipleChoice
        fields = (
            'id',
            'content',
            'question',
            'is_correct',
        )

    def __str__(self):
        return "%s" % (self.id)


class BlankQuestionContentSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=BlankQuestion.objects.order_by('id')
    )

    class Meta:
        model = BlankQuestionContent
        fields = (
            'id',
            'part_seq',
            'content',
            'question',
        )
        # read_only_fields = ('type',)

    def __str__(self):
        return "Q%s Number %s" % (self.question, self.seq)


class BlankSolutionSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=BlankQuestion.objects.order_by('id')
    )
    solution_set = serializers.ListField(
        child=serializers.CharField(max_length=255)
    )

    class Meta:
        model = BlankSolution
        fields = (
            'solution_set',
            'question'

        )

    def __str__(self):
        return "%s" % self.id


class McqSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(
        queryset=Assessment.objects.all()
    )
    type = serializers.IntegerField(default=Question.MCQ, read_only=True)

    choices = MultipleChoiceSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Mcq
        fields = (
            'id',
            'assessment',
            'number',
            'type',
            'description',
            'solution',
            'choices'
        )


class BlankQuestionSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(
        queryset=Assessment.objects.all()
    )
    type = serializers.IntegerField(default=Question.BLANKS, read_only=True)
    blank_parts = BlankQuestionContentSerializer(many=True, read_only=True)

    class Meta:
        model = BlankQuestion
        fields = (
            'id',
            'assessment',
            'number',
            'type',
            'description',
            'solution',
            'blank_parts',
        )


class ProgrammingQuestionSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(
        queryset=Assessment.objects.all()
    )
    type = serializers.IntegerField(
        default=Question.PROGRAMMING, read_only=True)

    class Meta:
        model = ProgrammingQuestion
        fields = (
            'id',
            'assessment',
            'number',
            'type',
            'description',
            'solution',
            'default_code',
            'code_signature',
        )


class CheckoffQuestionSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(
        queryset=Assessment.objects.all()
    )
    type = serializers.IntegerField(default=Question.CHECKOFF, read_only=True)

    class Meta:
        model = CheckoffQuestion
        fields = (
            'id',
            'assessment',
            'number',
            'type',
            'description',
            # 'solution',
            # 'default_code',
            # 'code_signature',
        )


# class QuestionSerializer(serializers.ModelSerializer):

#     """docstring for QuestionSerializer"""
#     assessment = serializers.PrimaryKeyRelatedField(
#         queryset=Assessment.objects.all()
#     )
#     blank_parts = BlankQuestionContentSerializer(many=True, read_only=True)
#     mcq_choices = MultipleChoiceSerializer(many=True, read_only=True)

#     class Meta:
#         model = Question
#         fields = (
#             'id',
#             'assessment',
#             'question_num',
#             'type',
#             'title',
#             'description',
#             'solution',
#             'default_code',
#             'blank_parts',
#             'mcq_choices',
#             'code_signature',
#         )


class CourseSerializer(serializers.ModelSerializer):

    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.order_by('id')
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

    type = serializers.ChoiceField(
        choices=Assessment.TYPE
    )

    programmingquestion_set = ProgrammingQuestionSerializer(
        read_only=True,
        many=True,
    )

    blankquestion_set = BlankQuestionSerializer(
        read_only=True,
        many=True,
    )
    mcq_set = McqSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Assessment
        fields = (
            'id',
            'type',
            'label',
            'start_datetime',
            'end_datetime',
            'course',
            'programmingquestion_set',
            'blankquestion_set',
            'mcq_set',
        )


class UnitTestSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=ProgrammingQuestion.objects.order_by('id')
    )
    inputs = serializers.ListField(
        child=serializers.CharField(max_length=255)
    )

    class Meta:
        model = UnitTest
        fields = (
            'id',
            'visibility',
            'type',
            'test_content',
            'inputs',
            'expected_output',
            'question',
        )
