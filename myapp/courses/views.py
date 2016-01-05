from rest_framework import viewsets, authentication, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import detail_route  # , list_route

from .serializers import (
    CourseSerializer,
    AssessmentSerializer,
    McqQuestionSerializer,
    BlankQuestionSerializer,
    ProgrammingQuestionSerializer,
    MultipleChoiceSerializer,
    BlankQuestionContentSerializer,
    QuestionSerializer,
    UnitTestSerializer,
)
from .models import (
    Course,
    Assessment,
    Question,
    MultipleChoice,
    BlankQuestionContent,
    UnitTest
)


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
    filter_fields = ['participants']


class AssessmentViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating assessment """
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    filter_fields = ['course']


class McqQuestionViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and Mcq Question """
    queryset = Question.objects.all().filter(type=Question.MCQ)
    serializer_class = McqQuestionSerializer


class BlankQuestionViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Blank Question """
    queryset = Question.objects.all().filter(type=Question.BLANKS)
    serializer_class = BlankQuestionSerializer


class ProgrammingQuestionViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Blank Question """
    queryset = Question.objects.all().filter(
        type=Question.PROGRAMMING)
    serializer_class = ProgrammingQuestionSerializer


class QuestionViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Question """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_fields = ['type', 'assessment']


class MultipleChoiceViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating multiple choice """
    queryset = MultipleChoice.objects.all()
    serializer_class = MultipleChoiceSerializer


class BlankQuestionContentViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating multiple choice """
    queryset = BlankQuestionContent.objects.all().order_by('part_seq')
    serializer_class = BlankQuestionContentSerializer


class UnitTestViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """
    API endpoint for listing and creating test case 
    """
    queryset = UnitTest.objects.all()
    serializer_class = UnitTestSerializer

    @detail_route(methods=['get'])
    def raw(self, request, pk=None):
        """
        Endpoint to get raw unittest code
        """
        
        unittest = self.get_object()
        test_code = unittest.get_test()
        return Response(test_code, status=200)

    @detail_route(methods=['get'])
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

        return Response(
            {"result": test_code},
            status=(200 if test_code['pass'] else 400)
        )
