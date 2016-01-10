from rest_framework import viewsets, authentication, permissions, filters
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from .serializers import *
from .models import *


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
    filter = ('submission')


class BlankEvaluationViewset(DefaultsMixin, viewsets.ReadOnlyModelViewSet):

    """ API endpoint for listing and creating Peer Rank Report """
    queryset = BlankEvaluation.objects.all()
    serializer_class = BlankEvaluationSerializer


class PeerRankViewset(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Peer Rank """
    queryset = PeerRank.objects.all()
    serializer_class = PeerRankSerializer


class AcademicReportViewset2(DefaultsMixin, viewsets.ViewSet):

    """
    API endpoint for getting academic Report
    required input: student id, course id

    Structure: 

    - AcademicReport:

        - student (unique_together with course)  
        - course  (unique_together with student)  
        - grade (bool)  
        - assessment_grade_report_set  
            - assessment  
            - grade  
            - override  
            - question_grade_report_set  
                - question_id (unique_together with question_type)  
                - question_type (unique_together with question_id)  
                - grade  
                - override  
                - submission_grade_report_set  
                    - submission_id (unique_together with submission_type)  
                    - submission_type (unique_together with submission_id)  
                    - grade  
                    - override  

    """
    # queryset = AcademicReport.objects.all()
    # serializer_class = AcademicReportSerializer
    filter_fields = ('student_id', 'course_id')

    def list(self, request):
        print request.data
        student_id = request.query_params.get('student_id', None)
        course_id = request.query_params.get('course_id', None)

        # queryset = AcademicReport.objects.all()
        # ar = get_object_or_404(queryset, pk=pk)
        # serializer = AcademicReportSerializer(ar)
        return Response(
            {
                'type1': {
                    'student_id': student_id,
                    'course_id': course_id
                },
                'type2': {
                    'student_id': student_id,
                    'course_id': course_id
                }
            }
        )


class AcademicReportViewset(DefaultsMixin, viewsets.ModelViewSet):

    """API endpoint for listing and creating Peer Rank"""
    queryset = AcademicReport.objects.all()
    serializer_class = AcademicReportSerializer
