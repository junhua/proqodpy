from rest_framework import viewsets, authentication, permissions, filters
from rest_framework.response import Response

from rest_framework.decorators import detail_route, list_route

from django.contrib.auth import get_user_model
from django.shortcuts import get_list_or_404

from .serializers import *
from .models import *
from djoser.serializers import UserSerializer

# import itertools


class DefaultsMixin(object):

    """ 
    Default settings for view auth, permissions, 
    filtering and pagination 
    """

    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
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


class AdminEditOnlyModelViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


class CourseViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating courses """
    queryset = Course.objects.order_by('date_created')
    serializer_class = CourseSerializer
    filter_fields = ['participants']

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

        queryset = get_user_model().objects.all()
        participants = get_list_or_404(queryset, courses=pk)

        serializer = UserSerializer(participants, many=True)

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        return super(CourseViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(CourseViewSet, self).retrieve(request, *args, **kwargs)


class AssessmentViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating assessment """
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    filter_fields = ['course']

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()


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

    """ API endpoint for listing and creating Blank Question """
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

    ## Endpoints

    raw() - return the raw code of the test case  
    run(code) - run test case against input code

    """

    queryset = UnitTest.objects.all()
    serializer_class = UnitTestSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()

    @detail_route(methods=['get'])
    def raw(self, request, pk=None):
        """
        Endpoint to get raw unittest code
        """

        unittest = self.get_object()
        test_code = unittest.get_test()
        return Response(test_code, status=200)

    @detail_route(methods=['get', 'post'])
    def run(self, request, pk=None):
        """
        Endpoint to allow execute unittests. 
        No record stored in the database.
        Expected input param: code


        Sample output for successful run:
        {
            pass: True,
            output: actual_output
        }

        Sample output for unsuccessful run:
        {
            pass: False,
            output: actual_output
        }

        Sample output for error:
        {
            pass: False,
            error: error_message
        }
        """
        code = request.query_params.get('code', None)

        if not code:
            return Response(
                {"pass": False,
                 "error": "code not found from params"
                 },
                status=404
            )

        unittest = self.get_object()

        test_code = unittest.run(code)

        print test_code

        return Response(
            {"result": test_code},
            status=(200 if test_code['pass'] else 400)
        )
