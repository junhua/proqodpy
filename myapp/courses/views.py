from rest_framework import viewsets, authentication, permissions, filters
from rest_framework.response import Response

from rest_framework.decorators import detail_route, list_route
# from djoser.serializers import UserSerializer
# from django.contrib.auth import get_user_model
from django.shortcuts import get_list_or_404, get_object_or_404

from .serializers import *
from .models import *

import datetime
import rest_framework_jwt

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
    queryset = Course.objects.order_by('date_created')
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
    Assessment will return question sets with submissions.
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
                Assessment.objects.all(), cohort_classes=cohort_class)
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


class BlankQuestionViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Blank Question """
    queryset = BlankQuestion.objects.all()
    serializer_class = BlankQuestionSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


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


class BlankQuestionContentViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating multiple choice """
    queryset = BlankQuestionContent.objects.all().order_by('part_seq')
    serializer_class = BlankQuestionContentSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class BlankSolutionViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating multiple choice """
    queryset = BlankSolution.objects.all()
    serializer_class = BlankSolutionSerializer

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

    # @detail_route(methods=['get'])
    # def raw(self, request, pk=None):
    #     """
    #     Endpoint to get raw unittest code
    #     """

    #     unittest = self.get_object()
    #     test_code = unittest.get_test()
    #     return Response(test_code, status=200)

    # @detail_route(methods=['get', 'post'])
    # def run(self, request, pk=None):
    #     """
    #     Endpoint to allow execute unittests.
    #     No record stored in the database.
    #     Expected input param: code

    #     Sample output for successful run:
    #     {
    #         pass: True,
    #         output: actual_output
    #     }

    #     Sample output for unsuccessful run:
    #     {
    #         pass: False,
    #         output: actual_output
    #     }

    #     Sample output for error:
    #     {
    #         pass: False,
    #         error: error_message
    #     }
    #     """
    #     code = request.query_params.get('code', None)

    #     if not code:
    #         return Response(
    #             {"pass": False,
    #              "error": "code not found from params"
    #              },
    #             status=404
    #         )

    #     unittest = self.get_object()

    #     test_code = unittest.run(code)

    #     print test_code

    #     return Response(
    #         {"result": test_code},
    #         status=(200 if test_code['pass'] else 400)
    #     )


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
