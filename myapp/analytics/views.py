from rest_framework import viewsets, authentication, permissions, filters
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from .serializers import *
from .models import *
from myapp.courses.models import *
from myapp.courses.serializers import *

import rest_framework_jwt

class DefaultsMixin(object):

    """ 
    Default settings for view auth, permissions, 
    filtering and pagination 
    """

    authentication_classes = (
        rest_framework_jwt.authentication.JSONWebTokenAuthentication,
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


class PerformanceReportViewset(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Performance Report """
    queryset = PerformanceReport.objects.all()
    serializer_class = PerformanceReportSerializer


class PeerRankReportViewset(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Peer Rank Report """
    queryset = PeerRankReport.objects.all()
    serializer_class = PeerRankReportSerializer
    filter = ('submission',)


class PeerRankViewset(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Peer Rank """
    queryset = PeerRank.objects.all()
    serializer_class = PeerRankSerializer


class QuestionGradeReportViewset(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Grade Report Entry """
    queryset = QuestionGradeReport.objects.all()
    serializer_class = QuestionGradeReportSerializer
    filter = ('student')

    # override index to show based on assessment
    def list(self, request):
        assessment = request.query_params.get("assessment")
        student = request.query_params.get("student")

        assessment_object = Assessment.objects.get(id=assessment)

        ids = []

        ids += list(assessment_object.programmingquestion_set.all().values_list('id', flat=True))
        ids += list(assessment_object.mcq_set.all().values_list('id', flat=True))
        ids += list(assessment_object.checkoffquestion_set.all().values_list('id', flat=True))
        ids += list(assessment_object.blankquestion_set.all().values_list('id', flat=True))

        queryset = QuestionGradeReport.objects.filter(student=student, question_id__in=ids)
        serializer = QuestionGradeReportSerializer(queryset, many=True)

        return Response(serializer.data)



