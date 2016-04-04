from django.contrib.auth import get_user_model
from rest_framework import serializers
from authnz.serializers import UserSerializer
from .models import *
from myapp.submissions.serializers import *

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


# class BlankQuestionContentSerializer(serializers.ModelSerializer):
#     question = serializers.PrimaryKeyRelatedField(
#         queryset=BlankQuestion.objects.all()
#     )

#     class Meta:
#         model = BlankQuestionContent
#         fields = (
#             'id',
#             'part_seq',
#             'content',
#             'question',
#         )
#         # read_only_fields = ('type',)

#     def __str__(self):
#         return "Q%s Number %s" % (self.question, self.seq)


class BlankSolutionSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=BlankQuestion.objects.all()
    )
    submissions = BlankSubmissionSerializer(
        many=True, read_only=True
        )
    from myapp.submissions.serializers import BlankSubmissionSerializer
    class Meta:
        model = BlankSolution
        fields = (
            'id',
            'seq',
            'content',
            'question',
            'submissions'
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
            'choices',
            'max_score',

        )



class McqWithSubmissionSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(
        queryset=Assessment.objects.all()
    )
    type = serializers.IntegerField(default=Question.MCQ, read_only=True)

    choices = MultipleChoiceSerializer(
        many=True,
        read_only=True
    )

    submissions = McqSubmissionSerializer(
        many=True, read_only=True)
    # progress = McqProgressSerializer(
    #     many=True, read_only=True)

    class Meta:
        model = Mcq
        fields = (
            'id',
            'assessment',
            'number',
            'type',
            'description',
            # 'solution',
            'choices',
            'max_score',
            'submissions',
            # 'progress'
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
            'solution_set',
            'max_score'
        )


class BlankQuestionWithSubmissionSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(
        queryset=Assessment.objects.all()
    )

    type = serializers.IntegerField(
        default=Question.BLANKS, read_only=True)

    blank_parts = BlankQuestionContentSerializer(
        many=True, read_only=True)

    solution_set = BlankSolutionSerializer(
        many=True, read_only=True)

    submissions = BlankSubmissionSerializer(
        many=True, read_only=True
    )

    # progress = BlankQuestionProgressSerializer(
    #     read_only=True
    # )

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
            'solution_set',
            'max_score',
            'submissions',
            # 'progress'
        )


class DynamicTestSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=ProgrammingQuestion.objects.all()
    )

    class Meta:
        model = DynamicTest
        fields = (
            'id',
            'visibility',
            'type',
            'test_content',
            'test_code',
            'question',
        )


class UnitTestSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=ProgrammingQuestion.objects.all()
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
            'unittests',
            'max_score'
        )


class ProgrammingQuestionWithSubmissionSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(
        queryset=Assessment.objects.all()
    )
    type = serializers.IntegerField(
        default=Question.PROGRAMMING, read_only=True)

    unittests = UnitTestSerializer(
        many=True, read_only=True
    )
    submissions = CodeSubmissionSerializer(
        many=True, read_only=True
    )

    # progress = ProgrammingQuestionProgressSerializer(
    #     read_only=True
    # )

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
            'unittests',
            'max_score',
            'submissions',
            # 'progress'
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
            'max_score'
            # 'solution',
            # 'default_code',
            # 'code_signature',
        )


class CheckoffQuestionWithSubmissionSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(
        queryset=Assessment.objects.all()
    )
    type = serializers.IntegerField(default=Question.CHECKOFF, read_only=True)

    # though single submissibon is allowed, using name submissions for
    # consistency with other types of questions
    submissions = CheckoffSubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = CheckoffQuestion
        fields = (
            'id',
            'assessment',
            'number',
            'type',
            'description',
            'max_score',
            'submissions'
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

    # cohort_classes = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=CohortClass.objects.all()
    # )

    cohort_classes = CohortClassSerializer(
        many=True, read_only=True
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


class AssessmentWithSubmissionSerializer(serializers.ModelSerializer):
    cohort_classes = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CohortClass.objects.all()
    )

    week = serializers.PrimaryKeyRelatedField(
        queryset=Week.objects.all()
    )

    type = serializers.ChoiceField(
        choices=Assessment.TYPE
    )

    programmingquestion_set = ProgrammingQuestionWithSubmissionSerializer(
        read_only=True,
        many=True,
    )

    blankquestion_set = BlankQuestionWithSubmissionSerializer(
        read_only=True,
        many=True,
    )
    mcq_set = McqWithSubmissionSerializer(
        read_only=True,
        many=True,
    )

    checkoffquestion_set = CheckoffQuestionWithSubmissionSerializer(
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
            'cohort_classes',
            'week',
            'programmingquestion_set',
            'blankquestion_set',
            'checkoffquestion_set',
            'mcq_set',
        )
