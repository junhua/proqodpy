from rest_framework import viewsets, authentication, permissions, filters, generics

from .serializers import (
    CourseSerializer,
    AssessmentSerializer,
    McqQuestionSerializer,
    BlankQuestionSerializer,
    ProgrammingQuestionSerializer,
    MultipleChoiceSerializer,
    BlankQuestionContentSerializer,
    QuestionSerializer,
)
from .models import (
    Course,
    Assessment,
    Question,
    MultipleChoice,
    BlankQuestionContent,
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
