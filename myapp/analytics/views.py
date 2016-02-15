from rest_framework import viewsets, authentication, permissions, filters
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from .serializers import *
from .models import *
from myapp.courses.models import *
from myapp.courses.serializers import *


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


# class GradeReportEntryViewset(DefaultsMixin, viewsets.ModelViewSet):

#     """ API endpoint for listing and creating Grade Report Entry """
#     queryset = GradeReportEntry.objects.all()
#     serializer_class = GradeReportEntrySerializer
#     filter = ('week', 'assessment', 'question', 'report')


class GradeReportViewset(DefaultsMixin,
                         viewsets.ModelViewSet):
    """ API endpoint for listing and creating Grade Report """
    queryset = GradeReport.objects.all()
    serializer_class = GradeReportSerializer
    filter = ('student', 'course')
