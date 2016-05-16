from rest_framework import viewsets, authentication, permissions, filters
from rest_framework.response import Response

from rest_framework.decorators import detail_route, list_route
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Q

from .serializers import *
from .models import *

import datetime
import rest_framework_jwt
import re

# import itertools


class DefaultsMixin(object):

    """
    Default settings for view auth, permissions,
    filtering and pagination
    """

    authentication_classes = (
        # authentication.BasicAuthentication,
        authentication.TokenAuthentication,
        rest_framework_jwt.authentication.JSONWebTokenAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
        # permissions.IsAdminUser,
    )
    paginate_by = 25
    paginate_by_param = "school"
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )


class CourseViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating courses """
    queryset = Course.objects.order_by('start_date')
    serializer_class = CourseSerializer
    filter_fields = ['course_batch', 'course_code', 'cohort_classes']

    permission_classes = [permissions.IsAuthenticated, ]

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()

    @detail_route(methods=['get'],
                  permission_classes=[permissions.IsAuthenticated, ])
    def participants(self, request, pk=None):
        """
        Endpoint to get participants by course
        """
        queryset = CohortClass.objects.all()
        cohort_classes = get_list_or_404(queryset, course=pk)
        serializer = CohortClassSerializer(cohort_classes, many=True)
        teachers, students = [], []
        for cc in serializer.data:
            teachers += cc.get('teachers')
            students += cc.get('students')

        teachers = list(set(teachers))
        students = list(set(students))

        # return Response(serializer.data)
        return Response({
            'teachers': teachers,
            'students': students
        })

    def list(self, request, *args, **kwargs):
        participant = request.query_params.get('participants')
        if participant:

            if request.user.user_type == 1 or request.user.is_admin == 1:
                queryset = Course.objects.all()
            else:
                queryset = Course.objects.filter(cohort_classes__students=participant).distinct()
            
            serializer = CourseSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return super(CourseViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(CourseViewSet, self).retrieve(request, *args, **kwargs)


class WeekViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating week """
    queryset = Week.objects.all()
    serializer_class = WeekSerializer
    filter_fields = ['course', 'number']

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class CohortClassViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating week """
    queryset = CohortClass.objects.all()
    serializer_class = CohortClassSerializer
    filter_fields = ['course', 'label', 'students', 'teachers']

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class AssessmentViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """
    API endpoint for listing and creating assessment.

    LAB, QUIZ, PROJECT, EXAM, COHORT, HOMEWORK, OPTIONAL = range(7)

    If sp_required is included in the header or param (e.g. True), 
    Assessment will return question sets with submissions and progress.
    This only applies to single assessment retrieval

    """
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    filter_fields = ['week', 'cohort_classes']

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()

    def list(self, request):

        user = request.user
        if user.user_type == 1 or user.is_admin == 1:
            queryset = Assessment.objects.all()
        else:
            queryset = Assessment.objects.filter(
                start_datetime__lte=datetime.datetime.now())

        serializer = AssessmentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = request.user

        if user.user_type == 1 or user.is_admin == 1:
            queryset = Assessment.objects.all()
        else:
            queryset = Assessment.objects.filter(
                start_datetime__lte=datetime.datetime.now())

        assessment = get_object_or_404(queryset, pk=pk)

        if request.query_params.get("sp_required"):
            serializer = AssessmentWithSubmissionSerializer(
                assessment)
        else:
            serializer = AssessmentSerializer(assessment)
        return Response(serializer.data)

    @list_route(methods=['get'], permission_classes=[permissions.IsAdminUser])
    def by_course(self, request):
        course = request.data.get(
            'course', None) or request.query_params.get('course', None)

        if not course:
            return Response([], status=400)

        try:
            course = get_object_or_404(Course, pk=course)
            course_serializer = CourseSerializer(course)

            cohort_classes = course_serializer.data.get('cohort_classes', None)

            cc_ids = [cc.get('id') for cc in cohort_classes]
            assmts = list(set(get_list_or_404(
                Assessment.objects.all(), cohort_classes__in=cc_ids)))
            serializer = AssessmentSerializer(assmts, many=True)
            return Response(serializer.data, status=200)
        except:
            return Response([], status=200)

    @list_route(methods=['get'],
                permission_classes=[permissions.IsAuthenticated]
                )
    def by_cohort_class(self, request):

        cohort_class = request.data.get(
            'cohort_class', None) or request.query_params.get(
            'cohort_class', None)

        if not cohort_class:
            return Response([], status=200)

        try:
            assmts = get_list_or_404(
                Assessment.objects.order_by("start_datetime").all(), cohort_classes=cohort_class)
            serializer = AssessmentSerializer(assmts, many=True)
            return Response(serializer.data, status=200)
        except:
            return Response([], status=200)


class McqViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and Mcq Question """
    queryset = Mcq.objects.all()
    serializer_class = McqSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class BlankSolutionViewSet(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
    """ API endpoint for getting blank solutions only after the user has submitted"""

    def get_queryset(self):
        user = self.request.user
        submitted_id = self.request.query_params.get('created_by', None)
        question_id = self.request.query_params.get('question', None)
        if (user.id == int(submitted_id)):
            return BlankQuestion.objects.filter(id=question_id, submissions__created_by_id=user.id)
        return BlankQuestion.objects.none()

    serializer_class = BlankSolutionsSerializer

    def get_permissions(self):
        return super(self.__class__, self).get_permissions()

    """ Don't index solutions"""

    def index(self, request):
        return Response([], status=400)


class BlankQuestionViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Blank Question """
    queryset = BlankQuestion.objects.all()
    serializer_class = BlankQuestionSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()

    @list_route(methods=['post'], permission_classes=[permissions.IsAdminUser, ])
    def create_with_content(self, request, pk=None):
        try:

            # scan through full_content for blanks <blank></blank> and split with regex.
            # the answers will be in odd indexes.

            full_content = request.data.get("fullContent", "")
            content = ""
            solutions = []

            chunked_array = [s.strip() for s in re.split(
                "<blank>|<\/blank>", full_content)]
            for index, item in enumerate(chunked_array):
                if index % 2:
                    # append if it is solution, add blank tags to content
                    solutions.append(item)
                    content += "<blank></blank>"
                else:
                    content += item
                    # it is content around the solution

            bq = BlankQuestion.objects.create(
                description=request.data["description"],
                number=request.data["number"],
                assessment_id=request.data["assessment"],
                content=content,
                full_content=full_content,
                solutions=solutions,
                type=2)
            bq.save()

            serializer = BlankQuestionSerializer(bq)

            return Response(serializer.data, status=200)
        except Exception as e:
            return Response(e.message, status=400)

    @detail_route(methods=['put'], permission_classes=[permissions.IsAdminUser, ])
    def update_with_content(self, request, pk=None):

        try:
            # scan through full_content for blanks <blank></blank> and split
            # with regex.

            full_content = request.data.get("full_content", "")
            content = ""
            solutions = []

            chunked_array = [s.strip() for s in re.split(
                "<blank>|<\/blank>", full_content)]

            for index, item in enumerate(chunked_array):
                if index % 2:
                    # it is solution, save to database
                    solutions.append(item)
                    content += "<blank></blank>"
                else:
                    content += item
                    # it is content around the solution

            BlankQuestion.objects.filter(id=pk).update(
                description=request.data["description"],
                content=content,
                full_content=full_content,
                solutions=solutions)

            return Response([], status=200)
        except Exception as e:
            return Response(e.message, status=400)


class ProgrammingQuestionViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Programming Question """
    queryset = ProgrammingQuestion.objects.all()
    serializer_class = ProgrammingQuestionSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class CheckoffQuestionViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Checkoff Question """
    queryset = CheckoffQuestion.objects.all()
    serializer_class = CheckoffQuestionSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class MultipleChoiceViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating multiple choice """
    queryset = MultipleChoice.objects.all()
    serializer_class = MultipleChoiceSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class UnitTestViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """
    API endpoint for listing and creating test case

    # Endpoints

    raw() - REMOVED, used to return the raw code of the test case
    run(code) - REMOVED, moved to /prog_qn_progress/run/

    """

    queryset = UnitTest.objects.all()
    serializer_class = UnitTestSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class DynamicTestViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """
    API endpoint for listing and creating test case

    # Endpoints

    raw() - REMOVED, used to return the raw code of the test case
    run(code) - REMOVED, moved to /prog_qn_progress/run/

    """

    queryset = DynamicTest.objects.all()
    serializer_class = DynamicTestSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()
