from django.contrib.auth import get_user_model
from django.shortcuts import get_list_or_404
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

    class Meta:
        model = BlankSolution
        fields = (
            'id',
            'seq',
            'content',
            'question',
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
            # 'solution',
            'choices'
        )


class BlankQuestionSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(
        queryset=Assessment.objects.all()
    )

    type = serializers.IntegerField(default=Question.BLANKS, read_only=True)

    blank_parts = BlankQuestionContentSerializer(many=True, read_only=True)

    solution_set = BlankSolutionSerializer(many=True, read_only=True)

    class Meta:
        model = BlankQuestion
        fields = (
            'id',
            'assessment',
            'number',
            'type',
            'description',
            # 'solution',
            'blank_parts',
            'solution_set'
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


class ProgrammingQuestionSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(
        queryset=Assessment.objects.all()
    )
    type = serializers.IntegerField(
        default=Question.PROGRAMMING, read_only=True)

    unittests = UnitTestSerializer(
        many=True, read_only=True
    )

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
            'unittests'
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


class CohortClassSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all()
    )
    teachers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.filter(user_type=1)
    )
    students = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.filter(user_type=0)
    )

    class Meta:
        model = CohortClass
        fields = (
            'id',
            'label',
            'teachers',
            'students',
            'course',
        )
        search_fields = ('school', )
        ordering_fields = ('school', 'department', 'id', )


class CourseSerializer(serializers.ModelSerializer):

    # participants = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=User.objects.order_by('id')
    # )

    cohort_classes = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CohortClass.objects.all()
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
            'cohort_classes',
            # 'participants',
        )
        search_fields = ('school', )
        ordering_fields = ('school', 'department', 'id', )


class WeekSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all()
    )

    class Meta:
        model = Week
        fields = (
            'id',
            'course',
            'number',
            'instruction'
        )
        search_fields = ('number', 'course')
        ordering_fields = ('number', )


class AssessmentSerializer(serializers.ModelSerializer):
    cohort_classes = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CohortClass.objects.all()
    )

    week = serializers.PrimaryKeyRelatedField(
        queryset=Week.objects.all()
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

    checkoffquestion_set = CheckoffQuestionSerializer(
        read_only=True,
        many=True,
    )

    # def create(self, validated_data):

    #     cohort_classes = get_list_or_404(
    #         CohortClass, pk__in=[cohort.id for cohort in validated_data['cohort_classes']])

    #     assessment = Assessment.objects.create(
    #         cohort_classes=cohort_classes,
    #         type=validated_data['type'],
    #         label=validated_data['label'],
    #         start_datetime=validated_data['start_datetime'],
    #         end_datetime=validated_data['end_datetime'],
    #         week=validated_data['week'],
    #     )

    #     return assessment

    class Meta:
        model = Assessment
        fields = (
            'id',
            'type',
            'label',
            'start_datetime',
            'end_datetime',
            'cohort_classes',
            'week',
            'programmingquestion_set',
            'blankquestion_set',
            'checkoffquestion_set',
            'mcq_set',
        )
